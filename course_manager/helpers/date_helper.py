from typing import Optional
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT_SHORT = '%Y-%m-%d'


def parse_date(date_str: str) -> Optional[datetime]:
    """Attempt to parse <date_str> into datetime using different formats.

    Return None if none of the formats match.
    """
    for date_format in [DATE_FORMAT, DATE_FORMAT_SHORT]:
        if (date := date_from_str(date_str, date_format)) is not None:
            return date
    return None


def date_from_str(date_str: str, date_format: str = DATE_FORMAT) -> Optional[datetime]:
    """Parse <date_str> into datetime with format <date_format>.

    Return None if the date cannot be parsed.
    """
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError:
        return None


def str_from_date(date: datetime, date_format: str = DATE_FORMAT) -> str:
    """Return the string representation of <date>, with format <date_format>.
    """
    return date.strftime(date_format)
