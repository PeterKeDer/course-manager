import re
from typing import cast, Optional
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

weekdays = [MO, TU, WE, TH, FR, SA, SU]
WEEKDAY_NAMES = [
    ('mon', 'monday'),
    ('tue', 'tuesday'),
    ('wed', 'wednesday'),
    ('thu', 'thursday'),
    ('fri', 'friday'),
    ('sat', 'saturday'),
    ('sun', 'sunday'),
]
WEEKDAYS_PATTERN = '|'.join('|'.join(names) for names in WEEKDAY_NAMES)

# Date specifier patterns
TODAY_PATTERN = re.compile('^today')
TOMORROW_PATTERN = re.compile('^(tmr|tomorrow)')
NEXT_DATE_PATTERN = re.compile('^next (week|month|year)')
NEXT_WEEKDAY_PATTERN = re.compile(f'^next ({WEEKDAYS_PATTERN})')
IN_X_DATE_PATTERN = re.compile(r'^in (\d+|a) (day|week|month|year)s?')
DATE_SPECIFIER_PATTERNS = [TODAY_PATTERN, TOMORROW_PATTERN, NEXT_DATE_PATTERN,
                           NEXT_WEEKDAY_PATTERN, IN_X_DATE_PATTERN]

# Time specifier patterns
MORNING_PATTERN = re.compile(' morning$')
NOON_PATTERN = re.compile(' noon$')
AFTERNOON_PATTERN = re.compile(' afternoon$')
EVENING_PATTERN = re.compile(' evening$')
NIGHT_PATTERN = re.compile(' night$')
MIDNIGHT_PATTERN = re.compile(' midnight$')
HH_MM_PATTERN = re.compile(r' (\d{1,2})(:(\d{2}))?\s*?(am|pm)?$')
NOW_PATTERN = re.compile(' (now|same time)$')
IN_X_TIME_PATTERN = re.compile(r' in (\d+) (min|minute|hr|hour)s?$')
TIME_SPECIFIER_PATTERNS = [MORNING_PATTERN, NOON_PATTERN, AFTERNOON_PATTERN,
                           EVENING_PATTERN, NIGHT_PATTERN, MIDNIGHT_PATTERN,
                           HH_MM_PATTERN, NOW_PATTERN, IN_X_TIME_PATTERN]


def parse(phrase: str) -> Optional[datetime]:
    """Try to parse date from readable, common phrases.
    A phrase consists of a date specifier followed by a time specifier.
    At least one must be specified.
    If date specifier is not given, default to today's date.
    If time specifier is not given, default to 00:00.

    Date specifiers:
    - today, tmr, tomorrow
    - next week, month, year, or a weekday (mon/monday, etc.)
    - in X day/week/month/year, where X is a number or 'a'

    Time specifiers:
    - morning, noon, afternoon, evening, night, midnight
    - HH:mm, or simply H or HH (for hour)
    - now / same time
    - in X min/minute/hr/hour, where X is a number
    """
    phrase = phrase.strip().lower()

    # Parse date and time from phrase
    d = _parse_readable_date_specifier(phrase)
    t = _parse_readable_time_specifier(phrase)

    if d is None and t is None:
        # Must have at least date or time specified
        return None

    return datetime.combine(d or date.today(),
                            t or time(0, 0, 0))


def _parse_readable_date_specifier(phrase: str) -> Optional[date]:
    """Parse the date specifier of phrase."""
    for pattern in DATE_SPECIFIER_PATTERNS:
        if (match := pattern.search(phrase)) is not None:
            if pattern == TODAY_PATTERN:
                return date.today()
            elif pattern == TOMORROW_PATTERN:
                return date.today() + relativedelta(days=+1)
            elif pattern == NEXT_DATE_PATTERN:
                specifier = match.group(1)
                start_date = date.today()

                # Set start date to start of month/year if necessary
                if specifier == 'month':
                    start_date = start_date.replace(day=1)
                elif specifier == 'year':
                    start_date = start_date.replace(day=1, month=1)

                return start_date + _get_delta(1, specifier)

            elif pattern == NEXT_WEEKDAY_PATTERN:
                weekday = _get_weekday(match.group(1))
                # Get the next weekday that is not today
                return date.today() + relativedelta(days=+1,
                                                    weekday=weekdays[weekday](1))
            elif pattern == IN_X_DATE_PATTERN:
                n = int(match.group(1))
                specifier = match.group(2)
                return date.today() + _get_delta(n, specifier)
    return None


def _parse_readable_time_specifier(phrase: str) -> Optional[time]:
    """Parse the time specifier of phrase."""
    for pattern in TIME_SPECIFIER_PATTERNS:
        if (match := pattern.search(phrase)) is not None:
            if pattern == MORNING_PATTERN:
                return time(9)
            elif pattern == NOON_PATTERN:
                return time(12)
            elif pattern == AFTERNOON_PATTERN:
                return time(15)
            elif pattern == EVENING_PATTERN:
                return time(18)
            elif pattern == NIGHT_PATTERN:
                return time(21)
            elif pattern == MIDNIGHT_PATTERN:
                return time(0)
            elif pattern == HH_MM_PATTERN:
                hour = int(match.group(1))
                minute = int(match.group(3) or '0')

                if match.group(4) == 'pm' and hour < 12:
                    # Note 12 pm hour is also 12
                    return time(hour + 12, minute)

                return time(hour, minute)

            elif pattern == NOW_PATTERN:
                return datetime.now().time()
            elif pattern == IN_X_TIME_PATTERN:
                n = int(match.group(1))
                specifier = match.group(2)
                return cast(datetime, datetime.now() + _get_delta(n, specifier)).time()


def _get_delta(n: int, specifier: str) -> relativedelta:
    """Return the time delta representing n times specifiers amount of time."""
    # Note: the keyword argument passed into `relativedelta` is important to have s at the end
    # If not, it will set that component to n instead of incrementing
    if specifier == 'min' or specifier == 'minute':
        return relativedelta(minutes=n)
    elif specifier == 'hr' or specifier == 'hour':
        return relativedelta(hours=n)
    elif specifier == 'day':
        return relativedelta(days=n)
    elif specifier == 'week':
        return relativedelta(weeks=n)
    elif specifier == 'month':
        return relativedelta(months=n)
    elif specifier == 'year':
        return relativedelta(years=n)
    else:
        return relativedelta()


def _get_weekday(weekday_str: str) -> int:
    """Get the weekday int associated to weekday_str. Return -1 if the string is invalid."""
    for i, names in enumerate(WEEKDAY_NAMES):
        if weekday_str in names:
            return i
    return -1
