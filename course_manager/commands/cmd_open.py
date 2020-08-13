import os
import click
from typing import Optional
from course_manager.cli import get_params, args
from course_manager.helpers import path_helper, project_helper


@click.command('open')
@get_params(args.COURSE_CODE, args.PROJECT_ID_OPTIONAL, args.FILE_OPTIONAL)
def cmd_open(course_code: str, project_id: Optional[str], file: Optional[str]):
    """Open projects or files.

    Paths can be used to specify directory or files within projects to open.
    """
    if project_id is None:
        # Open course
        path = str(path_helper.get_path(course_code))
        os.system(f'open "{path}"')
    elif project_helper.project_exists(course_code, project_id):
        if file is None:
            # Open project with open_method in settings
            # If not set or error reading settings, default to open by path
            settings = project_helper.read_project_settings(course_code, project_id)
            path = path_helper.get_path(course_code, project_id)

            if settings is not None and settings.open_method is not None:
                # Use project's open_method if possible
                os.system(f'cd "{path}"; {settings.open_method}')
            else:
                os.system(f'open "{path}"')
        else:
            path = str(path_helper.get_path(course_code, project_id, file))
            os.system(f'open "{path}"')
    else:
        # Project does not exist
        click.echo(f'The project with id "{project_id}" does not exist'
                   f'for the course "{course_code}".')
