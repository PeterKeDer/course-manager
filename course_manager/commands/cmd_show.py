import sys
import click
from typing import Optional
from course_manager.cli import get_params, args, opts
from course_manager.helpers import course_helper, project_helper, date_helper


@click.command('show')
@get_params(opts.ARCHIVED, args.COURSE_CODE_OPTIONAL, args.PROJECT_ID_OPTIONAL)
def cmd_show(archived: bool, course_code: Optional[str], project_id: Optional[str]):
    """Show courses, projects, and more.

    When given:

    - No arguments: show all courses by default. If --archived is given, show archived courses instead.

    - Only course_code: show info related to course

    - course_code and project_id: show info related to specific project from course
    """
    if course_code is None:
        _show_all_courses(archived)
    elif project_id is None:
        _show_course(course_code)
    else:
        _show_project(course_code, project_id)


def _show_all_courses(archived: bool):
    """Show all courses.

    If archived is True, show archived courses instead.
    """
    # TODO: show more than just course codes
    if archived:
        courses = course_helper.get_archived_course_codes()
    else:
        courses = course_helper.get_course_codes()

    if len(courses) == 0:
        if archived:
            click.echo('There are currently no archived courses.')
        else:
            click.echo('There are currently no courses.')
    else:
        for course_code in courses:
            click.echo('=' * 20)
            _show_course(course_code)


def _show_course(course_code: str):
    """Show info related to course with <course_code>.

    If course does not exist, display message and exit with status code 1.
    """
    if not course_helper.course_exists(course_code):
        click.echo(f'The course with code "{course_code}" does not exist.')
        sys.exit(1)

    click.echo(f'Course: {course_code}')
    click.echo('Projects:')

    for project_id in project_helper.get_project_ids(course_code):
        click.echo(f'- {project_id}')

    # TODO: show due dates?
    # TODO: add templates here after implementing


def _show_project(course_code: str, project_id: str):
    """Show info related to project with <project_id> from course with <course_code>."""
    click.echo(f'{course_code}: {project_id}')

    if not course_helper.course_exists(course_code):
        click.echo(f'The course with code "{course_code}" does not exist.')
        sys.exit(1)

    if not project_helper.project_exists(course_code, project_id):
        click.echo(f'The project "{project_id}" does not exist.')
        sys.exit(1)

    settings = project_helper.read_project_settings(course_code, project_id)

    if settings is None:
        click.echo(f'Failed to read settings file for project "{project_id}".\n'
                   'The file could have invalid format or does not exist.')
        sys.exit(1)

    click.echo(f'Project id: {project_id}')
    click.echo(f'Name: {settings.name}')

    if settings.due_date is not None:
        date_str = date_helper.str_from_date(settings.due_date)
        click.echo(f'Due date: {date_str}')

    if settings.open_method is not None:
        click.echo(f'Open method: "{settings.open_method}"')

