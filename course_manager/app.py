import click
from course_manager.commands import commands


@click.group()
def run():
    """Course manager CLI application.
    """


# Add each command to the group
for cmd in commands:
    run.add_command(cmd)
