import configparser
import course_manager.helpers.path_helper as paths

CONFIG_FILE = 'config.ini'

KEY_BASE_DIRECTORY = 'base_directory'

ALLOWED_CONFIG_KEYS = {
    KEY_BASE_DIRECTORY,
}


class ConfigKeyInvalidError(Exception):
    """Exception indicating that a config key is invalid.
    """


def _read_config():
    """Read configurations from files.

    If the file does not exist, initialize with default options.
    """
    data_sets = _config.read(CONFIG_FILE)

    if len(data_sets) == 0:
        # The file does not exist, will initialize with default values
        _initialize_config()


def _write_config():
    """Write configurations to the file.
    """
    with open(CONFIG_FILE, 'w') as configfile:
        _config.write(configfile)


def _initialize_config():
    """Initialize configurations with default values.
    """
    _config['DEFAULT'] = {
        KEY_BASE_DIRECTORY: paths.DEFAULT_BASE_DIRECTORY,
    }
    _write_config()


def get_config(key: str) -> str:
    """Get the configuration with key <item>.

    Raise ConfigKeyInvalidError if the key does not exist in config.
    """
    lower_key = key.lower()
    if lower_key not in ALLOWED_CONFIG_KEYS:
        raise ConfigKeyInvalidError

    return _config['DEFAULT'][lower_key]


def set_config(key: str, value: str):
    """Set the configuration of key <key> to <value>.

    Raise ConfigKeyInvalidError if the config key is not allowed.
    """
    lower_key = key.lower()
    if lower_key not in ALLOWED_CONFIG_KEYS:
        raise ConfigKeyInvalidError

    _config['DEFAULT'][lower_key] = value
    _write_config()


_config = configparser.ConfigParser()
_read_config()
