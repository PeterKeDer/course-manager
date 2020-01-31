import click

_arg = click.argument

CONFIG_NAME = _arg('config_name', type=str)
COURSE_CODE = _arg('course_code', type=str)
COURSE_CODES = _arg('course_codes', nargs=-1)
COURSE_CODE_OPTIONAL = _arg('course_code', type=str, required=False)
FILE_OPTIONAL = _arg('file', type=str, required=False)
PATHS = _arg('paths', type=str, nargs=-1)
PROJECT_ID = _arg('project_id', type=str)
PROJECT_ID_OPTIONAL = _arg('project_id', type=str, required=False)
