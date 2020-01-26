import click
from typing import Optional
from course_manager.cli import *
from course_manager.helpers.config_helper import config_helper, ConfigKeyInvalidError


@click.command('config')
@get_params(args.CONFIG_NAME, opts.WRITE)
def cmd_config(config_name: str, write: Optional[str]):
    """Read or write configurations.

    If <write> is given, it will write its value to the config.

    Otherwise, echo the current value of the config.
    """
    try:
        if write is None:
            # Read config
            click.echo(config_helper[config_name])
        else:
            # Write config
            config_helper[config_name] = write

    except ConfigKeyInvalidError:
        # The key is not allowed
        click.echo(f'Invalid config key "{config_name}".')
        exit(1)
