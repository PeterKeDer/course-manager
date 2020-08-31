from course_manager.helpers import date_helper, readable_date_parser

def date_validator(s: str):
    """Validator for due date prompt."""
    is_valid, res, msg = False, None, None

    if s.strip() == '':
        is_valid, res = True, None
    elif (date := date_helper.parse_date(s)) is not None:
        is_valid, res = True, date
    elif (date := readable_date_parser.parse(s)) is not None:
        is_valid, res = True, date
    else:
        msg = ('Please enter a date with one of the common formats, such as "YYYY-MM-DD".\n'
               'Or use a readable format such as "next Monday at 5pm", "tmr", etc.\n'
               'Leave blank to not set a due date.')

    return is_valid, res, msg
