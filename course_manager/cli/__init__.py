from course_manager.cli.repeat_prompt import repeat_prompt, Validator, ValidateResult
from course_manager.cli import arguments as args, options as opts


def get_params(*decorators):
    """Decorator to get CLI arguments and options as parameters for function.

    Composes an arbitrary number of decorators into a single decorator.
    """
    def func(f):
        for dec in reversed(decorators):
            f = dec(f)
        return f
    return func



