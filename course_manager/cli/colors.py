from typing import List
from random import shuffle

COLORS = [
    'white',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'black',
]


def get_colors(n: int) -> List[str]:
    """Get <n> different colors.

    If n is greater than the amount of colors available, then there will be duplicates.
    """
    extras = n % len(COLORS)
    copies = n // len(COLORS)

    return COLORS * copies + COLORS[:extras]
