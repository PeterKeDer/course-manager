from typing import Optional
from datetime import datetime, date
from dateutil.parser import parse, ParserError

DATE_FORMAT_FULL = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT_DATE_TIME = '%Y-%m-%d %H:%M'
DATE_FORMAT_DATE = '%Y-%m-%d'
DATE_FORMAT_TIME = '%H:%M'


def parse_date(date_str: str) -> Optional[datetime]:
    """Attempt to parse <date_str> into datetime using different formats.

    Return None if none of the formats match.
    """
    try:
        return parse(date_str)
    except ParserError:
        return None


def date_from_str(date_str: str, date_format: str = DATE_FORMAT_FULL) -> Optional[datetime]:
    """Parse <date_str> into datetime with format <date_format>.

    Return None if the date cannot be parsed.
    """
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError:
        return None


def str_from_date(date_obj: datetime, date_format: str = DATE_FORMAT_FULL) -> str:
    """Return the string representation of <date>, with format <date_format>."""
    return date_obj.strftime(date_format)


def is_today(date_obj: datetime) -> bool:
    """Return True iff date is today."""
    return date_obj.date() == date.today()
