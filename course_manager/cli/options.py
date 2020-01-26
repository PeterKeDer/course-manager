import click

_opt = click.option

WRITE = _opt('-w', '--write', type=click.STRING,
             help='If given, the content to write to config.')
