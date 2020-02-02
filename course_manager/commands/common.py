import sys
import click
from course_manager.helpers import course_helper


def check_course_exists(course_code: str):
    """Check that the course with <course_code> exist.

    If it does not exist, display message and exit with status code 1.
    """
    if not course_helper.course_exists(course_code):
        click.echo(f'The course with code "{course_code}" does not exist.')
        sys.exit(1)
