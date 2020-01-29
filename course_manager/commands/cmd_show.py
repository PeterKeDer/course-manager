import click
from course_manager.cli import get_params, opts
from course_manager.helpers import course_helper


@click.group('show')
def cmd_show():
    """Show courses, projects, and more."""


@cmd_show.command('courses')
@get_params(opts.ARCHIVED)
def cmd_courses(archived: bool):
    """Display current or archived course codes."""
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
        for course in courses:
            click.echo(course)
