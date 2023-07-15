from typing import Dict, Any
import tomllib
import logging

logger = logging.getLogger('core')


__ALL__ = ['config']

class TomlConfigParser:
    """
    A class for parsing and accessing values from a TOML configuration file.

    Attributes:
        _shared_state (dict): A shared state dictionary for managing the
        configuration file path and loaded data.
        _config_file_path (str): The path to the TOML configuration file.
        config_data (Dict[str, Any]): The loaded configuration data as
        a dictionary.
    """
    _shared_state = {}

    def __init__(self, config_file_path):
        """
        Initialize the TomlConfigParser instance with the specified
        configuration file path.
        """
        self.__dict__ = self._shared_state
        if not self._shared_state:
            self._config_file_path = config_file_path
            self.config_data = self.load_config_data()

    def load_config_data(self) -> Dict[str, Any]:
        """
        Load the configuration data from the current configuration file.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the configuration file contains invalid TOML syntax.
        """
        try:
            with open(self._config_file_path, 'rb') as settings_file:
                config = tomllib.load(settings_file)
        except FileNotFoundError:
            msg = f"The `{self._config_file_path}` file does not exist!"
            logger.critical(msg)
            raise FileNotFoundError(msg)
        except tomllib.TOMLDecodeError as e:
            msg = f"The `{self._config_file_path}` file contains invalid TOML syntax! Error: {e}"
            logger.critical(msg)
            raise ValueError(msg)
        return config

    def get_value(self, category: str, key: str=None, default=None) -> Any:
        """
        Retrieve the value associated with the specified key from the
        configuration data. and return it.. or.
        If key is None, return the whole category.
        If default is provided, return it if the key is not found in the config.

        Returns:
            Any: The value associated with the specified key, the whole
            category, or the default value.ˇ
        """
        conf = self._get_inners(category)
        if key:
            conf = conf.get(key, None)
        return conf

    def _get_inners(self, categories: str|list, config: dict=None):
        """
        Recursively retrieve the nested configuration data by splitting
        the categories string.

        Returns:
            Any: The nested configuration data.
        """
        if not config:
            config = self.config_data
        if isinstance(categories, str):
            categories = categories.split('.')
        while not len(categories) == 1:
            config = config.get(categories[0])
            del categories[0]
            return self._get_inners(categories, config)
        return config.get(categories[0])

config = TomlConfigParser('settings.toml')
