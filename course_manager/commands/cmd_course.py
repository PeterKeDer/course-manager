import sys
import click
from course_manager.cli import get_params, args
from course_manager.helpers import course_helper


@click.group('course')
def cmd_course():
    """Add, remove, archive, or unarchive courses."""


@cmd_course.command('add')
@get_params(args.COURSE_CODE)
def cmd_course_add(course_code: str):
    """Add a new course."""
    course_code = _validate_course_code(course_code)

    if course_helper.course_exists(course_code):
        click.echo(f'A course with code "{course_code}" already exists.')
    elif course_helper.course_archived(course_code):
        click.echo(f'A course with code "{course_code} is already in archive."')
    else:
        course_helper.add_course(course_code)


@cmd_course.command('remove')
@get_params(args.COURSE_CODE)
def cmd_course_remove(course_code: str):
    """Remove a course."""
    course_code = _validate_course_code(course_code)
    _check_course_exists(course_code)

    msg = (f'Are you sure you want to remove "{course_code}"?\n'
           'All of its contents will be permanently deleted and cannot be restored.\n')

    # Repeats prompt 2 times in case of error
    click.confirm(msg, abort=True)
    click.confirm(msg, abort=True)

    course_helper.remove_course(course_code)
    click.echo(f'"{course_code}" is removed from courses.')


@cmd_course.command('archive')
@get_params(args.COURSE_CODE)
def cmd_course_archive(course_code: str):
    """Move a course into archive folder."""
    course_code = _validate_course_code(course_code)
    _check_course_exists(course_code)

    course_helper.archive_course(course_code)
    click.echo(f'The course with code {course_code} is moved into archive.')


@cmd_course.command('unarchive')
@get_params(args.COURSE_CODE)
def cmd_course_unarchive(course_code: str):
    """Move an archived course back into courses."""
    course_code = _validate_course_code(course_code)
    _check_course_archived(course_code)

    course_helper.unarchive_course(course_code)
    click.echo(f'The course with code {course_code} is moved from archive to courses.')


def _validate_course_code(course_code: str) -> str:
    """Validate the course code. Returns the validated course code.

    If the course code is not valid, display message and exist with status code 1.
    """
    lower = course_code.lower()
    if not course_helper.course_code_is_valid(lower):
        click.echo(f'The course code "{course_code}" is invalid.\n'
                   'A course code can only contain letters, numbers, or underscores.')
        sys.exit(1)
    return lower


def _check_course_exists(course_code: str):
    """Check that the course with <course_code> exist.

    If it does not exist, display message and exit with status code 1.
    """
    if not course_helper.course_exists(course_code):
        click.echo(f'The course with code "{course_code}" does not exist.')
        sys.exit(1)


def _check_course_archived(course_code: str):
    """Check that the course with <course_code> is archived.

    If it is not in archive, display message and exit with status code 1.
    """
    if not course_helper.course_archived(course_code):
        click.echo(f'The course with code "{course_code}" does not exist in archive.')
        sys.exit(1)
