import click

_opt = click.option

ARCHIVED = _opt('-a', '--archived', is_flag=True,
                help='Option to echo archived courses instead of current courses.')
TEMPLATE = _opt('-t', '--template', type=str,
                help='The template to use for the project.')
WRITE = _opt('-w', '--write', type=str,
             help='If given, the content to write to config.')
