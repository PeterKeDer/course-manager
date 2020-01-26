import click

_arg = click.argument

CONFIG_NAME = _arg('config_name', type=click.STRING)
COURSE_CODE = _arg('course_code', type=click.STRING)
PATH = _arg('path', type=click.STRING)
