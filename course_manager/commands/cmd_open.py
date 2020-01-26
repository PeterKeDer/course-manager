import click
from course_manager.cli import *


@click.command('open')
@get_params(args.COURSE_CODE, args.PATH)
def cmd_open(course_code: str, path: str):
    """Command for opening files.
    """
    # TODO
    print(course_code, path)
