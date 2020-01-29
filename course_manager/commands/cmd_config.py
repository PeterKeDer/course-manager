import click
from typing import Optional
from course_manager.cli import get_params, args, opts
from course_manager.helpers import config_helper, path_helper


@click.command('config')
@get_params(args.CONFIG_NAME, opts.WRITE)
def cmd_config(config_name: str, write: Optional[str]):
    """Read or write configurations.

    If <write> is given, it will write its value to the config.

    Otherwise, echo the current value of the config.
    """
    try:
        value = config_helper.get_config(config_name)

        if write is None:
            # Read config
            click.echo(value)
        else:
            # Write config
            config_helper.set_config(config_name, write)

            _post_write_handler(config_name, prev=value, new=write)

    except config_helper.ConfigKeyInvalidError:
        # The key is not allowed
        click.echo(f'Invalid config key "{config_name}".')
        exit(1)


def _post_write_handler(config_name: str, prev: str, new: str):
    """Special handlers for writing certain configurations."""
    if config_name.lower() == config_helper.KEY_BASE_DIRECTORY and prev != new:
        # Prompt to rename base directory
        if click.confirm('Base directory was changed. '
                         'Do you want to move existing courses to the new directory?'):
            renamed = path_helper.rename_base_directory(prev, new)
            if renamed:
                click.echo(f'Courses moved from {prev} to {new}!')
            else:
                click.echo(f'Unable to move courses, the file/directory {prev} already exists.')
