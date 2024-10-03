"""
A fallback for time zone look ups for when pytz or dateutils cannot find an appropriate timezone

Some environments may not have this information
"""
import typing
timezones: typing.Mapping[str, str] = {
    # Eastern Time Zone
    'EST': 'America/New_York',      # Eastern Standard Time (UTC-5)
    'EDT': 'America/New_York',      # Eastern Daylight Time (UTC-4)

    # Central Time Zone
    'CST': 'America/Chicago',       # Central Standard Time (UTC-6)
    'CDT': 'America/Chicago',       # Central Daylight Time (UTC-5)

    # Mountain Time Zone
    'MST': 'America/Denver',        # Mountain Standard Time (UTC-7) and Arizona
    'MDT': 'America/Denver',        # Mountain Daylight Time (UTC-6)

    # Pacific Time Zone
    'PST': 'America/Los_Angeles',   # Pacific Standard Time (UTC-8)
    'PDT': 'America/Los_Angeles',   # Pacific Daylight Time (UTC-7)

    # Alaska Time Zone
    'AKST': 'America/Anchorage',    # Alaska Standard Time (UTC-9)
    'AKDT': 'America/Anchorage',    # Alaska Daylight Time (UTC-8)

    # Hawaii-Aleutian Time Zone
    'HST': 'Pacific/Honolulu',      # Hawaii Standard Time (UTC-10, No DST)
    # Note: Hawaii does not observe Daylight Saving Time

    # Samoa Time Zone (American Samoa)
    'SST': 'Pacific/Pago_Pago',     # Samoa Standard Time (UTC-11, No DST)

    # Chamorro Time Zone (Guam, Northern Mariana Islands)
    'ChST': 'Pacific/Guam',         # Chamorro Standard Time (UTC+10, No DST)
}
"""
A mapping between all US time zone abbreviations to their formal names. Only use as a fallback.

Only codes from the USA are used since USGS RDB is a format used by a USGS Government Agency
"""
