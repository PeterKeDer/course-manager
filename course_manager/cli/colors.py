from typing import List
from random import shuffle

COLORS = [
    'black',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
    'bright_black',
    'bright_red',
    'bright_green',
    'bright_yellow',
    'bright_blue',
    'bright_magenta',
    'bright_cyan',
    'bright_white',
]


def get_random_colors(n: int) -> List[str]:
    """Get <n> random, different colors.

    If n is greater than the amount of colors available, then there will be duplicates.
    """
    extras = n % len(COLORS)
    copies = n // len(COLORS)

    colors_copy = COLORS[:]
    shuffle(colors_copy)

    return COLORS * copies + colors_copy[:extras]
