import click

_opt = click.option

ARCHIVED = _opt('-a', '--archived', is_flag=True,
                help='Option to echo archived courses instead of current courses.')
WRITE = _opt('-w', '--write', type=click.STRING,
             help='If given, the content to write to config.')
