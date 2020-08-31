import sys
import click
from course_manager.helpers import course_helper, project_helper


def check_course_exists(course_code: str):
    """Check that the course with <course_code> exists.

    If it does not exist, display message and exit with status code 1.
    """
    if not course_helper.course_exists(course_code):
        click.echo(f'The course with code "{course_code}" does not exist.')
        sys.exit(1)


def check_project_exists(course_code: str, project_id: str):
    """Check that the project with id <project_id> exists in <course_code> exist.

    If it does not exist, display message and exit with status code 1.
    """
    if not project_helper.project_exists(course_code, project_id):
        click.echo(f'The project with id "{project_id}" does not exist'
                   f'for the course "{course_code}".')
