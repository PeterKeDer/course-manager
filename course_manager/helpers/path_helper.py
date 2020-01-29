from typing import Union
from pathlib import Path
import course_manager.helpers.config_helper as config_helper

HOME_PATH = Path.home()
DEFAULT_BASE_DIRECTORY = 'courses'


def get_home_path(*paths: Union[str, Path]) -> Path:
    """Get the path from home of the system."""
    return Path(HOME_PATH, *paths)


def get_base_path() -> Path:
    """Get the path to the base directory of courses.
    """
    return Path(HOME_PATH, config_helper.get_config(config_helper.KEY_BASE_DIRECTORY))


def get_path(*paths: Union[str, Path]) -> Path:
    """Get path extended from base directory, with components <paths>.
    """
    return Path(get_base_path(), *paths)


def rename_base_directory(prev: str, new: str) -> bool:
    """Rename the base directory from prev to new.

    Return False if the new directory already exists and will abort rename.

    Otherwise, return True.
    """
    if Path(HOME_PATH, new).exists():
        return False

    Path(HOME_PATH, prev).rename(Path(HOME_PATH, new))
    return True
