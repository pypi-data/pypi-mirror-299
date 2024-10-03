"""
Defines the classes and tools used to read and interpret USGS RDB files
"""
from __future__ import annotations

import io
import os
import pathlib
import typing
import re
from dataclasses import dataclass
from dataclasses import field

import numpy
import pandas
import pytz
import requests

from dateutil.parser import parse as parse_date
from dateutil.tz import gettz
from pandas._typing import ReadCsvBuffer

from .timezones import timezones

SITE_TIMESERIES_ROW: re.Pattern = re.compile(r"# Data provided for site (?P<site_code>\d+)\s*")
"""The regular expression detailing the line that defines the site code for the following data"""

PARAMETER_CODE_PATTERN: re.Pattern = re.compile(r"#\s+\d+\s+(?P<pcode>\d{5})\s+(?P<description>.+)")
"""The regular expression detailing the line that links a parameter code to a description"""

SITE_CODE_PATTERN: re.Pattern = re.compile(r"#\s+[a-zA-Z_]+\s+(?P<site_code>\d+)\s+(?P<site_name>.+)")
"""The pattern describing how to link values within a line stating a site code to its name"""

TS_ID_PREFIX_PATTERN = re.compile(r"^\d+_")
"""
A regular expression that matches on the unneccesary TS_ID that is prepended to the variable name in an RDB time 
series. This helps clean up strings like '2761_00060' and '174788_00065' to reveal '00060' for stream flow
and '00065' for stage. Without this clean up step, the column names from the description won't match the column name 
in the table
"""

HEADER_ROW_PATTERN = re.compile(r"^[a-z]([a-z_0-9]+\s*)+$")
"""The pattern that matches on the two lines detailing the header of a dataset within an RDB file"""

DATATYPE_ROW_PATTERN = re.compile(r"(\d+[sdn]\t?)+")
"""A regular expression that identifies the row that details the column length and its data type"""

DATATYPE_PATTERN = re.compile(r"\d+(?P<datatype>[sdn])")
"""The regular expression that identifies the data type of a column within an RDB file"""

HEADING_EXPLANATION_PATTERN = re.compile(
    r"#\s+(?P<column>[a-z0-9_]+)\s+(\.\.\.|--)\s+(?P<description>[-A-Za-z _.\[()\]]+)"
)
"""A regular expression that links a column name to its description - this will mostly be found in daily statistics"""

DEFAULT_DELIMITER: typing.Final[str] = "\t"
"""The character used to separate values in columns"""

DEFAULT_SITE_NAME = "Default"
"""The name of the 'default' table in an RDB dataset that doesn't subdivide its contents"""

T = typing.TypeVar("T")
"""A generic type"""

NWIS_DATETIME_FORMAT: typing.Final[str] = "%Y-%m-%d %H:%M"

DATATYPE_FUNCTIONS = {
    "s": str,
    "n": lambda val: float(val) if "." in val else int(val),
    "d": parse_date
}
"""Defines functions to use when converting a read string into an intended type"""

DATATYPE_TYPES = {
    "s": str,
    "n": float,
}
"""Defines how to interpret a given data type"""

ApplicationFunction = typing.Union[
    typing.Callable[[pandas.Series], typing.Any],
    str,
    typing.List[typing.Union[typing.Callable[[pandas.Series], typing.Any], str]],
    typing.MutableMapping[
        typing.Hashable,
        typing.Union[
            typing.Callable[[pandas.Series], typing.Any],
            str,
            typing.List[typing.Union[typing.Callable[[pandas.Series], typing.Any], str]],
        ]
    ]
]


class FrameTransformation:
    """
    A mutator that will call a function and assign the results to the given column name

    Inputs to the function will look something like:

        +----------+------------------+
        | Index    | Value            |
        +==========+==================+
        | site_no  | 02339495         |
        +----------+------------------+
        | datetime | 2023-11-16 11:15 |
        +----------+------------------+
        | tz_cd    | CST              |
        +----------+------------------+
        | ( ... )  | ( ... )          |
        +----------+------------------+

    And values may be accessed like:

        >>> row['site_no'] == '02339495'
        True
    """
    def __init__(
        self,
        column_name: str,
        transformation: typing.Callable[[pandas.Series], typing.Any]
    ):
        if not isinstance(transformation, typing.Callable):
            raise TypeError(f"Transformation functions must be callables - received {type(transformation)} instead")

        self.__function = transformation
        """The function that will generate a series of new values along axis 1 of a dataframe"""

        self.__column_name = column_name
        """The column name to assign the results of the function to"""

    def __call__(self, frame: pandas.DataFrame) -> pandas.DataFrame:
        frame[self.__column_name] = frame.apply(self.__function, axis=1)
        return frame


class NormalizeTimeZoneUnawareTransformation(FrameTransformation):
    """
    A transformation that will transform a date into UTC then back to the local time zone to ensure
    that all received dates are in the same timezone
    """
    def __init__(self, to_column_name: str, date_column: str, timezone_code_column):
        """
        Constructor

        :param to_column_name: The name of the column to assign the normalized dates to
        :param date_column: The column that has the date information to convert (such as 'datetime')
        :param timezone_code_column: The column that has the timezone information for the dates (such as 'tz_cd')
        """
        super().__init__(column_name=to_column_name, transformation=self.to_utc_unaware)
        self.__date_column = date_column
        self.__timezone_code_column = timezone_code_column

    def to_utc_unaware(self, row: pandas.Series) -> pandas.Timestamp:
        """
        Convert the date in the given row to UTC normalized naive date

        The row will look something like:

        +----------+------------------+
        | Index    | Value            |
        +==========+==================+
        | site_no  | 02339495         |
        +----------+------------------+
        | datetime | 2023-11-16 11:15 |
        +----------+------------------+
        | tz_cd    | CST              |
        +----------+------------------+
        | ( ... )  | ( ... )          |
        +----------+------------------+

        :param row: An option containing data from a row of the input frame
        :return: A naive datetime timestamp converted into implicit UTC
        """
        date: pandas.Timestamp = row[self.__date_column]
        timezone_code = row[self.__timezone_code_column]
        timezone = gettz(timezone_code)

        if timezone is None:
            timezone = timezones.get(timezone_code)

            if timezone is None:
                raise ValueError(f"{timezone_code} is not a valid timezone code")
        localized_date = date.tz_localize(timezone)
        utc_date = localized_date.tz_convert(pytz.UTC)
        return utc_date.tz_localize(None)


@dataclass
class RDBTable:
    """The raw structure containing values from an RDB file"""
    parse_dates: typing.List[str] = field(default_factory=list)
    """The names of fields that should be parsed as dates"""

    dtypes: typing.Dict[str, typing.Type] = field(default_factory=dict)
    """A mapping of column names to their intended data types"""

    data_lines: typing.List[str] = field(default_factory=list)
    """The individual lines of text that form this table"""

    columns: typing.Dict[str, str] = field(default_factory=dict)
    """Mapping between column names and their description"""

    site_code: typing.Optional[str] = field(default=None)
    """The USGS site code of the location assigned to this data"""

    location_name: typing.Optional[str] = field(default=None)
    """The name of the location assigned to this data"""

    post_processing_functions: typing.List[FrameTransformation] = field(default_factory=list, hash=False)
    """Optional functions used to perform post-processing tasks"""

    delimiter: typing.Optional[str] = field(default=DEFAULT_DELIMITER, hash=True, repr=False)
    """The character delimiter used to separate columns when parsing the input data as CSV"""

    __frame: typing.Optional[pandas.DataFrame] = field(default=None, hash=False, init=False, repr=False)
    """The dataframe created from the input data"""

    def add_line(self, text: typing.Union[typing.Dict[str, typing.Any], str], at_beginning: bool = False):
        """
        Add a line of data to the table
        :param text: The line of text to add
        :param at_beginning: Whether to add the text to the beginning of the data
        """
        if isinstance(text, typing.Mapping) and at_beginning:
            raise ValueError(
                f"Cannot add line to RDBTable '{self}' - passing a dictionary of values and instructing to "
                "insert the values at the beginning at incompatible operations"
            )

        if isinstance(text, typing.Dict):
            if not text:
                return

            line_values = [
                text.get(column_name, '')
                for column_name in self.columns
            ]

            new_line = self.delimiter.join(line_values)
            self.data_lines.append(new_line)
        elif at_beginning:
            self.data_lines.insert(0, text)
        else:
            self.data_lines.append(text)

        self.__frame = None

    def vectorize(self, function: typing.Callable[[pandas.Series, ...], pandas.Series], *columns: str) -> pandas.Series:
        """
        Semi-vectorize a function across columns in the dataframe

        This is not true vectorization but may be more efficient than `apply`

        :param function: The function to call on the given columns
        :param columns: The columns to pass in as each parameter
        :return: A new series created by the function
        """
        missing_columns: typing.List[str] = []

        for column in columns:
            if column not in self.frame.columns:
                missing_columns.append(column)

        if missing_columns:
            raise KeyError(
                f"Cannot call {function.__qualname__} on {self} - the following column(s) are not "
                f"available within this table"
            )
        return numpy.vectorize(function)(*[self.frame[column] for column in columns])

    @property
    def frame(self) -> pandas.DataFrame:
        """
        The table represented as a dataframe
        """
        if self.__frame is not None:
            return self.__frame

        # Build the dataframe by constructing CSV text and parsing it with pandas
        buffer: ReadCsvBuffer[str] = io.StringIO(os.linesep.join(self.data_lines))

        creation_kwargs = {
            "na_values": [
                "Dis",          # Record has been discontinued at the measurement site.
                "Rat",          # Rating being developed
                "Mnt",          # Site undergoing maintenance
            ]
        }

        if self.dtypes:
            creation_kwargs['dtype'] = self.dtypes

        if self.parse_dates:
            creation_kwargs['parse_dates'] = self.parse_dates
            creation_kwargs['date_format'] = NWIS_DATETIME_FORMAT

        frame = pandas.read_csv(
            buffer,
            delimiter=self.delimiter,
            **creation_kwargs
        )

        for transformation in self.post_processing_functions:
            frame = transformation(frame)

        self.__frame = frame
        return frame

    def __getitem__(
        self,
        index: typing.Union[slice, typing.Hashable, typing.Iterable, pandas.Series, pandas.DataFrame]
    ) -> typing.Union[pandas.Series, pandas.DataFrame, numpy.ndarray[typing.Any, numpy.signedinteger]]:
        return self.frame[index]

    def __setitem__(
        self,
        index: typing.Union[slice, pandas.Series, pandas.DataFrame, pandas.Series, pandas.Index, numpy.ndarray],
        value: typing.Any
    ) -> None:
        self.frame[index] = value

    def __len__(self) -> int:
        return len(self.data_lines) - 1 if self.data_lines else 0

    def apply(
        self,
        func: ApplicationFunction,
        axis: typing.Literal[0, 1, 'index', 'columns'] = 0,
        raw: bool = False,
        result_type: typing.Literal['expand', 'reduce', 'broadcast'] = None,
        args: tuple = (),
        by_row: typing.Literal[False, "compat"] = "compat",
        engine: typing.Literal["python", "numba"] = "python",
        engine_kwargs: typing.Dict[str, typing.Any] = None,
        **kwargs
    ) -> pandas.Series:
        """
        Call the apply function on the internal dataframe

        See https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html for details

        :param func: The function(s) to call on the internal dataframe
        :param axis: 0 to apply the function to each column, 1 to apply to each row
        :param raw: Determines if the row or column is passed as a Series or ndarray
        :param result_type: How the results will be shaped. Returns a pandas.Series by default
        :param args: Positional arguments to pass to `func` alongside the data
        :param by_row: If a collection of functions is passed, determines if the whole series should be passed to them
        :param engine: Allows the use of `numba` to use JIT code. May speed up operations on large datasets.
        :param engine_kwargs: Keyword arguments for when numba is used
        :param kwargs: Keywords passed to the given function(s)
        :return: A new series made up of the values created from the given function(s)
        """
        return self.frame.apply(
            func,
            axis=axis,
            raw=raw,
            result_type=result_type,
            args=args,
            by_row=by_row,
            engine=engine,
            engine_kwargs=engine_kwargs,
            **kwargs
        )

    def copy(self) -> pandas.DataFrame:
        """
        Create a copy of the internal dataframe
        """
        return self.frame.copy()

    def __str__(self) -> str:
        return f"{self.site_code or self.location_name}: {self.columns}"


def parse_rdb(
        text: typing.Union[str, bytes],
        frame_processing_functions: typing.Iterable[FrameTransformation] = None,
        *,
        delimiter: str = DEFAULT_DELIMITER
) -> typing.Tuple[typing.Mapping[str, RDBTable], typing.Optional[RDBTable]]:
    default_data: typing.Optional[RDBTable] = None
    timeseries: typing.Dict[str, RDBTable] = {}

    # Assign an empty collection to the frame processing functions to allow for safe iteration
    if frame_processing_functions is None:
        frame_processing_functions = []

    if isinstance(text, bytes):
        text = text.decode()

    locations: typing.Optional[typing.Dict[str, str]] = None
    """A mapping of location names to their table keys"""

    columns: typing.List[str] = list()
    """All column names for all tables"""

    headings: typing.Dict[str, str] = dict()
    """Heading information gathered from comments prior to tables within RDB sources"""

    active_site = DEFAULT_SITE_NAME
    """The name of the site currently being parsed"""

    active_timeseries = None
    """The lines of data for the time series currently being parsed"""

    found_data = False
    """Whether raw data to parse has been encountered"""

    for line in text.splitlines():
        # Check to see if we haven't found any data and we've hit a line like:
        # '#    USGS 02453000 BLACKWATER CREEK NEAR MANCHESTER AL'
        # This tells us that the file being parsed will have a location with code
        #   '02453000' named 'BLACKWATER CREEK NEAR MANCHESTER AL'
        if not found_data and SITE_CODE_PATTERN.match(line):
            match = SITE_CODE_PATTERN.match(line)
            if locations is None:
                locations = {}

            locations[match.group("site_code")] = match.group("site_name")
            continue

        # Check to see if a line details that the following data will belong to a particular location.
        # This will match on lines like:
        #   '# Data provided for site 02339495'
        # You will see this on observations, but not necessarily statistics
        if SITE_TIMESERIES_ROW.match(line):
            match = SITE_TIMESERIES_ROW.match(line)
            active_site = match.group("site_code")
            continue

        # Check to see if a line has been hit that details a TS_ID, a parameter code and a description.
        # This will match on lines like:
        #   '#    2760        00065     Gage height, feet'
        # And tell us what '00065' means.
        if PARAMETER_CODE_PATTERN.match(line):
            match = PARAMETER_CODE_PATTERN.match(line)
            headings[match.group("pcode")] = match.group("description")
            continue

        # Check to see if a line has been hit that details all contained columns within a dataset
        # Will match on lines like:
        #   'agency_cd	site_no	datetime	tz_cd	2761_00060	2761_00060_cd	2760_00065	2760_00065_cd'
        # This indicates that raw data is about to follow
        if HEADER_ROW_PATTERN.match(line):
            columns = [
                TS_ID_PREFIX_PATTERN.sub("", entry)
                for entry in line.split(delimiter)
            ]
            found_data = False

            # Determine the name of a location being parsed. Data such as statistics won't have a name
            location_name: str = locations.get(active_site) if locations and active_site in locations else None

            # Create a new table of data that will be parsed
            active_timeseries = RDBTable(
                site_code=active_site,
                location_name=location_name,
                columns=headings,
                post_processing_functions=frame_processing_functions,
                delimiter=delimiter
            )

            # Set the new time series to the default if this is unnamed data or attach it to the map of time
            # series if there might be more than one table
            if active_site == DEFAULT_SITE_NAME:
                default_data = active_timeseries
            else:
                timeseries[active_site] = active_timeseries

            # Add the columns into the new set of data for the table
            active_timeseries.add_line(delimiter.join(columns), at_beginning=True)

            # We won't necessarily know we're in a new set of data when we encounter new headings,
            # so clear this so that previously added data won't contaiminate data that comes after this
            # time series is parsed
            headings = {}
            continue

        # Check to see if we've hit a line that maps a column name to what its data describes
        # Matches on lines like:
        #   '# month_nu    ... The month for which the statistics apply.'
        # And
        #   '# day_nu      ... The day for which the statistics apply.'
        if not found_data and HEADING_EXPLANATION_PATTERN.match(line):
            match = HEADING_EXPLANATION_PATTERN.match(line)
            headings[match.group("column")] = match.group("description")
            continue

        # Check to see if we've hit a line that describes the what data type each column is
        # Matches on lines like:
        #   '5s	15s	20d	6s	14n	10s	14n	10s'
        # The meanings are:
        #   - s: string
        #   - n: number (either int or float)
        #   - d: datetime
        # The number before it is the number of columns on the line that the raw data occupies
        if DATATYPE_ROW_PATTERN.match(line):
            # Move on if we're already parsing data. This happens rarely, but data is sometimes sent out of
            # order like this
            if found_data:
                continue

            # Gather each identified data type indicator
            datatypes = [
                match.group("datatype")
                for match in DATATYPE_PATTERN.finditer(line)
            ]

            # Match the indicated data types with their column names or record which columns need to be parsed as
            # dates
            for column, datatype in zip(columns, datatypes):
                if datatype == 'd':
                    active_timeseries.parse_dates.append(column)
                elif datatype in DATATYPE_TYPES:
                    active_timeseries.dtypes[column] = DATATYPE_TYPES[datatype]
            continue

        # If this line starts with a '#' and doesn't match one of the previous patterns,
        # it's a comment and we can skip it
        if line.startswith("#"):
            continue

        # We are officially parsing lines of data, so set the flag stating so
        found_data = True
        active_timeseries.add_line(line)
    return timeseries, default_data


class RDB:
    """
    A container for all read tables from an RDB file

    Structured like a dictionary of individual tables of data since each RDB file may contain multiple sets of data

    Most RDB files may only have one set of data, but retrieving multiple locations at once may return data that simply
    looks like one table of information appended after a few newlines to another table of information
    """
    @classmethod
    def from_path(
        cls,
        path: pathlib.Path,
        frame_processing_functions: typing.Iterable[FrameTransformation] = None
    ) -> RDB:
        """
        Load RDB data from a file

        :param path: The path to the RDB file
        :param frame_processing_functions: Optional functions used to perform post-processing tasks
        :return: A new RDB structure
        """
        text_data = path.read_text()
        return cls(text_data, frame_processing_functions)

    @classmethod
    def from_url(
        cls,
        url: str,
        frame_processing_functions: typing.Iterable[FrameTransformation] = None,
        **request_kwargs
    ) -> RDB:
        """
        Load RDB data from a URL

        :param url: The address of the RDB data
        :param frame_processing_functions:  Optional functions used to perform post-processing tasks
        :param request_kwargs: Keyword arguments to pass to requests.get
        :return: A new RDB structure
        """
        with requests.get(url, **request_kwargs) as response:
            if response.status_code < 400:
                return cls(response.text, frame_processing_functions=frame_processing_functions)
            raise Exception(str(response.text))

    def __init__(
        self,
        text: typing.Union[str, bytes],
        frame_processing_functions: typing.Iterable[FrameTransformation] = None,
        *,
        delimiter: str = DEFAULT_DELIMITER,
    ):
        """
        Constructor

        :param text: Raw text or bytes containing the required data
        :param frame_processing_functions:  Optional functions used to perform post-processing tasks
        """
        general_data, default_data = parse_rdb(
            text=text,
            frame_processing_functions=frame_processing_functions,
            delimiter=delimiter
        )

        self.__default_data = default_data
        """An unnamed RDB table - used with datasets like statistics that don't subdivide data by location"""

        self.__timeseries: typing.Dict[str, RDBTable] = general_data or {}
        """Individually grouped time series data from the RDB source"""

        if default_data:
            self.__timeseries[self.__default_data.site_code] = self.__default_data

    def __getitem__(self, key: str) -> RDBTable:
        """
        Retrieve a table that corresponds with the given key

        :param key: The name of the table to retrieve
        :return: An RDBTable instance with data related to the given key
        """
        return self.__timeseries[key]

    def __len__(self):
        """
        The number of time series loaded from the RDB source
        """
        return max(len(self.__timeseries), 1 if self.__default_data else 0)

    @property
    def data(self) -> typing.Optional[pandas.DataFrame]:
        """
        Unnamed data from a single dataset loaded from the RDB source
        """
        return self.__default_data.frame if self.__default_data else None

    def get(self, key: str, __default: T = None) -> typing.Union[RDBTable, T]:
        """
        Get a loaded RDB dataset from the RDB source

        :param key: The name of the dataset to retrieve
        :param __default: What to return if the data isn't present
        :return: An RDB table or None if the data isn't present
        """
        if key.lower() == DEFAULT_SITE_NAME.lower():
            return self.__default_data
        return self.__timeseries.get(key, __default)

    def items(self) -> typing.Sequence[typing.Tuple[str, RDBTable]]:
        items = [*self.__timeseries.items()]
        if self.__default_data:
            items.append((DEFAULT_SITE_NAME, self.__default_data))
        return items

    def keys(self) -> typing.Sequence[str]:
        keys = list(self.__timeseries.keys())
        if self.__default_data:
            keys.append(DEFAULT_SITE_NAME)
        return keys

    def values(self) -> typing.Sequence[RDBTable]:
        values = list(self.__timeseries.values())
        if self.__default_data:
            values.append(self.__default_data)
        return values

    def __iter__(self):
        return iter(self.__timeseries)



