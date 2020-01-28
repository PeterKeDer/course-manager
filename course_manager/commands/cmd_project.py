import sys
import click
from typing import Optional
from course_manager.cli import *
from course_manager.models.project_settings import ProjectSettings
from course_manager.helpers import course_helper, project_helper


@click.group('project')
def cmd_project():
    """Create, manage, or remove projects.
    """


@cmd_project.command('create')
@get_params(args.COURSE_CODE, args.PROJECT_ID, opts.TEMPLATE)
def cmd_project_create(course_code: str, project_id: str, template: Optional[str]):
    """Create a project. User will be prompted with options.

    If template is given, will create the project with template.
    """
    # TODO: handle template

    if not course_helper.course_exists(course_code):
        click.echo(f'The course with code "{course_code}" does not exist.')
        sys.exit(1)

    if not project_helper.project_id_is_valid(project_id):
        click.echo('The project id is invalid.\n'
                   'A project id can only contain letters, numbers, or underscores.')
        sys.exit(1)

    if project_helper.project_exists(course_code, project_id):
        click.echo(f'The project with id "{project_id}" already exists in "{course_code}".')
        sys.exit(1)

    # TODO: prompt for settings
    name = click.prompt('name', type=str)

    settings = ProjectSettings(name, project_id, None, 'open .')

    project_helper.create_project(course_code, settings)


@cmd_project.command('delete')
@get_params(args.COURSE_CODE, args.PROJECT_ID)
def cmd_command_delete(course_code: str, project_id: str):
    pass

