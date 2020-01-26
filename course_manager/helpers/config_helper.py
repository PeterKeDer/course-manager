import configparser
import course_manager.helpers.path_helper as paths

CONFIG_FILE = 'config.ini'
ALLOWED_CONFIG_KEYS = {
    'base_directory'
}


class ConfigKeyInvalidError(Exception):
    """Exception indicating that a config key is invalid.
    """


class ConfigHelper:
    file_name: str
    config: configparser.ConfigParser

    def __init__(self, file_name: str = CONFIG_FILE):
        """Initialize config helper from file <file_name>.

        If the file does not exist, it will be created with default values.
        """
        self.file_name = file_name
        self.config = configparser.ConfigParser()
        self._read_config()

    def _read_config(self):
        """Read configurations from files.

        If the file does not exist, initialize with default options.
        """
        data_sets = self.config.read(self.file_name)

        if len(data_sets) == 0:
            # The file does not exist, will initialize with default values
            self._initialize_config()

    def _write_config(self):
        """Write configurations to the file.
        """
        with open(CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

    def _initialize_config(self):
        """Initialize configurations with default values.
        """
        self.config['DEFAULT'] = {
            'base_directory': paths.DEFAULT_BASE_DIRECTORY,
        }

        self._write_config()

    def __getitem__(self, key: str) -> str:
        """Get the configuration with key <item>.

        Raise ConfigKeyInvalidError if the key does not exist in config.
        """
        lower_key = key.lower()
        if lower_key not in ALLOWED_CONFIG_KEYS:
            raise ConfigKeyInvalidError

        return self.config['DEFAULT'][lower_key]

    def __setitem__(self, key: str, value: str):
        """Set the configuration of key <key> to <value>.

        Raise ConfigKeyInvalidError if the config key is not allowed.
        """
        lower_key = key.lower()
        if lower_key not in ALLOWED_CONFIG_KEYS:
            raise ConfigKeyInvalidError

        self.config['DEFAULT'][lower_key] = value
        self._write_config()


# The default config helper
config_helper = ConfigHelper()
