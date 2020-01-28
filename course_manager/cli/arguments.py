import click

_arg = click.argument

CONFIG_NAME = _arg('config_name', type=str)
COURSE_CODE = _arg('course_code', type=str)
PATH = _arg('path', type=str)
PROJECT_ID = _arg('project_id', type=str)
