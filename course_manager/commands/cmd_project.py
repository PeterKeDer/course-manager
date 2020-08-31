import sys
import click
from typing import Optional
from course_manager.cli import get_params, args, opts, repeat_prompt, date_validator
from course_manager.models.project_settings import ProjectSettings
from course_manager.helpers import course_helper, project_helper
from course_manager.constants import MAX_PROJECT_NAME_CHARS, MAX_PROJECT_ID_CHARS
from course_manager.commands.common import check_course_exists


@click.group('project')
def cmd_project():
    """Create, manage, or remove projects."""


@cmd_project.command('add')
@get_params(args.COURSE_CODE, opts.TEMPLATE)
def cmd_project_add(course_code: str, template: Optional[str]):
    """Add a project to the course with given course code. User will be prompted with options.

    If template is given, will create the project with template.
    """
    check_course_exists(course_code)

    # TODO: Should adjust based on template?
    project_id = repeat_prompt('Project id', _get_project_id_validator(course_code))
    name = repeat_prompt('Name', _project_name_validator, default=project_id)
    due_date = repeat_prompt('Due date', repeat_prompt.date_validator)
    open_method = click.prompt('Open method', default='open .', type=str)

    # Create settings based on given options
    settings = ProjectSettings(name, project_id, due_date, open_method)

    # Create project
    project_helper.create_project(course_code, settings)
    click.echo(f'Project "{project_id}" created successfully!')


@cmd_project.command('remove')
@get_params(args.COURSE_CODE, args.PROJECT_ID)
def cmd_command_remove(course_code: str, project_id: str):
    """Remove the project with given course code and project id."""
    _check_project_exists(course_code, project_id)

    msg = (f'Are you sure you want to delete project "{project_id}"?\n'
           'All of its contents will be permanently deleted and cannot be restored.\n')

    # Repeats prompt 2 times in case of error
    click.confirm(msg, abort=True)
    click.confirm(msg, abort=True)

    project_helper.delete_project(course_code, project_id)
    click.echo(f'The project "{project_id}" is is deleted from "{course_code}".')


def _check_project_exists(course_code: str, project_id: str):
    """Check that the course with <course_code> exists, and it has a project with id <project_id>.

    If either is False, then display message and exit with status code 1.
    """
    check_course_exists(course_code)

    if not project_helper.project_exists(course_code, project_id):
        click.echo(f'The project with id "{project_id} does not exist in "{course_code}".')
        sys.exit(1)


def _get_project_id_validator(course_code: str):
    """Get the validator for project id, given <course_code>."""
    def project_id_validator(s: str):
        """Validator for project id prompt."""
        value: Optional[str]
        is_valid, value, msg = False, None, None

        if not project_helper.project_id_is_valid(s):
            msg = ('The project id is invalid.\n'
                   'A project id can only contain letters, numbers, or underscores with at most'
                   f'{MAX_PROJECT_ID_CHARS} characters.')
        elif project_helper.project_exists(course_code, s):
            msg = f'The project with id "{s}" already exists in "{course_code}".'
        else:
            is_valid, value = True, s

        return is_valid, value, msg

    return project_id_validator


def _project_name_validator(s: str):
    """Validator for project name prompt."""
    value: Optional[str]
    is_valid, value, msg = False, None, None

    if not project_helper.project_name_is_valid(s):
        msg = ('The project name is invalid.\n'
               f'A project name must have between 1 and {MAX_PROJECT_NAME_CHARS} characters.')
    else:
        is_valid, value = True, s

    return is_valid, value, msg

