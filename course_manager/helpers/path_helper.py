from pathlib import Path

HOME_PATH = Path.home()
DEFAULT_BASE_DIRECTORY = 'courses'


def get_base_path() -> Path:
    return Path(HOME_PATH, DEFAULT_BASE_DIRECTORY)


def get_path(*paths: str) -> Path:
    return Path(get_base_path(), *paths)
