import click

_opt = click.option

ARCHIVED = _opt('--archived', is_flag=True,
                help='Option to echo archived courses.')
COURSE_CODE = _opt('-c', '--course-code', type=str,
                   help='Course code of the course.')
TEMPLATE = _opt('-t', '--template', type=str,
                help='The template to use for the project.')
WRITE = _opt('-w', '--write', type=str,
             help='If given, the content to write to config.')
