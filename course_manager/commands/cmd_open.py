import click
from course_manager.cli import get_params, args


@click.command('open')
@get_params(args.COURSE_CODE, args.PATH)
def cmd_open(course_code: str, path: str):
    """Open projects or files.
    """
    # TODO
    print(course_code, path)
