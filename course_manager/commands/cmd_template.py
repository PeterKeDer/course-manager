import sys
import click
from typing import Optional
from course_manager.cli import get_params, args, opts
from course_manager.helpers import template_helper
from course_manager.commands.common import check_course_exists


@click.group('template')
def cmd_template():
    """Create, delete, and edit templates."""


@cmd_template.command('create')
@get_params(args.TEMPLATE, opts.COURSE_CODE)
def cmd_template_create(template: str, course_code: Optional[str]):
    """Create a new template.

    If course_code is given, create template for that specific course.
    """
    # TODO: add base template option
    _validate_template_name(template)

    if template_helper.template_exists(template, course_code):
        click.echo(f'Template with name "{template}" already exists.')
        sys.exit(1)

    if course_code is not None:
        check_course_exists(course_code)

    template_helper.create_template(template, course_code)


@cmd_template.command('delete')
@get_params(args.TEMPLATE, opts.COURSE_CODE)
def cmd_template_delete(template: str, course_code: Optional[str]):
    """Delete an existing template.

    If course_code is given, delete the template from that course.
    """
    _validate_template_name(template)

    if not template_helper.template_exists(template):
        click.echo(f'Template with name "{template}" does not exist.')
        sys.exit(1)

    if course_code is not None:
        check_course_exists(course_code)

    msg = (f'Are you sure you want to delete the template "{template}"?\n'
           'All of its contents will be permanently deleted and cannot be restored.\n')

    click.confirm(msg, abort=True)
    click.confirm(msg, abort=True)

    template_helper.delete_template(template, course_code)


def _validate_template_name(template: str):
    """Check that the template name is valid.

    If it is invalid, display message and exit with status code 1.
    """
    if not template_helper.template_name_is_valid(template):
        click.echo(f'Invalid template name "{template}".\n'
                   'A valid template name contains only letters, numbers, and underscores.')
        sys.exit(1)
