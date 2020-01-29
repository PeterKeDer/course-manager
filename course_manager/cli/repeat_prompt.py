import click
from typing import Callable, Optional, TypeVar, Tuple

T = TypeVar('T')
ValidateResult = Tuple[bool, Optional[T], Optional[str]]
Validator = Callable[[str], ValidateResult]


def repeat_prompt(text: str, validator: Validator, *args, **kwargs) -> T:
    """Prompt user for a value and validate it with validator, which returns a
    tuple containing (is valid, validated value, fail message).

    If validator returns False and a fail message, will display the fail message.

    Repeatedly prompt until validator returns valid.

    :param text: text to print
    :param validator: function to validate a given input from user
    :return the validated input from user
    """
    def prompt():
        s = click.prompt(text, default='', show_default=False, *args, **kwargs)
        return validator(s)

    is_valid, value, fail_msg = prompt()
    while not is_valid:
        if fail_msg is not None:
            click.echo(fail_msg)

        is_valid, value, fail_msg = prompt()

    return value
