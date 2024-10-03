# PyRDB
A python library used to create tables from the RDB USGS format

Details about how RDB is meant to be built and interpretted can be found at: https://pubs.usgs.gov/of/2003/ofr03123/6.4rdb_format.pdf

## Example

```python
import pyrdb

statistical_thresholds = pyrdb.RDB.from_url(
    "https://waterservices.usgs.gov/nwis/stat/?format=rdb&sites=02339495,02342500&statReportType=daily&statTypeCd=all"
)
print(type(statistical_thresholds.data))
print(statistical_thresholds.data)
print(type(statistical_thresholds['Default']))
```

```
<class 'pandas.core.frame.DataFrame'>
data.data
     agency_cd   site_no parameter_cd     ts_id  ... p75_va  p80_va  p90_va  p95_va
0         USGS  02339495        00060    1974.0  ...    202     243     998     NaN
1         USGS  02339495        00060    1974.0  ...    278     371     729     NaN
2         USGS  02339495        00060    1974.0  ...    435     525    1080     NaN
3         USGS  02339495        00060    1974.0  ...    492     560     873     NaN
4         USGS  02339495        00060    1974.0  ...    319     378     701     NaN
...        ...       ...          ...       ...  ...    ...     ...     ...     ...
1459      USGS  02342500        00065  174790.0  ...   2.06    2.31    4.01    4.48
1460      USGS  02342500        00065  174790.0  ...   1.93    2.58    3.34    4.23
1461      USGS  02342500        00065  174790.0  ...   2.27    2.49    3.66    8.42
1462      USGS  02342500        00065  174790.0  ...    2.2    2.61    4.23    6.32
1463      USGS  02342500        00065  174790.0  ...   2.36    2.55    3.51    4.97
[1464 rows x 24 columns]
<class 'pyrdb.rdb.RDBTable'>
```

```python
import pyrdb
from pathlib import Path

observations = pyrdb.RDB.from_path(
    Path("test/resources/alabama.rdb"),
    frame_processing_functions=[
        pyrdb.NormalizeTimeZoneUnawareTransformation(
            to_column_name="datetime",
            date_column="datetime",
            timezone_code_column="tz_cd"
        )
    ]
)
print(observations['02342937'])
```

```
02342937: {'00060': 'Discharge, cubic feet per second', '00065': 'Gage height, feet', '72254': 'Water velocity reading from field sensor, feet per second', '72255': 'Mean water velocity for discharge computation, feet per second'}
```

```python
print(observations['02342937'].frame)
```

```
   agency_cd   site_no            datetime  ... 72254_cd  72255 72255_cd
0       USGS  02342937 2023-11-16 17:15:00  ...        P   0.01        P
1       USGS  02342937 2023-11-16 17:30:00  ...        P  -0.02        P
2       USGS  02342937 2023-11-16 17:45:00  ...        P   0.00        P
3       USGS  02342937 2023-11-16 18:00:00  ...        P   0.04        P
4       USGS  02342937 2023-11-16 18:15:00  ...        P   0.05        P
..       ...       ...                 ...  ...      ...    ...      ...
90      USGS  02342937 2023-11-17 15:45:00  ...        P  -0.02        P
91      USGS  02342937 2023-11-17 16:00:00  ...        P  -0.16        P
92      USGS  02342937 2023-11-17 16:15:00  ...        P  -0.11        P
93      USGS  02342937 2023-11-17 16:30:00  ...        P   0.02        P
94      USGS  02342937 2023-11-17 16:45:00  ...        P   0.08        P
[95 rows x 12 columns]
```
```python
print(observations['02342937']['00060'])
```
```
0      4.14
1     -7.01
2      0.41
3     15.30
4     18.90
      ...  
90    -6.70
91   -65.50
92   -44.70
93     8.07
94    34.60
Name: 00060, Length: 95, dtype: float64
```