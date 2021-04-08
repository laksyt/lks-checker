from pathlib import Path
from typing import Callable, Iterable

import yaml
from yaml.parser import ParserError

from laksyt.config.args import Args
from laksyt.config.profiles import Profiles


class Config:
    """Encapsulates configurable parameters of the application

    Extracts the name of active profile, then loads and parses the appropriate
    .yml configuration file.
    """

    def __init__(
            self,
            profiles: Profiles = Profiles(),
            cl_args: list[str] = None
    ):
        """Orchestrates retrieval and parsing of active profile config"""
        self._profiles = profiles

        self._args = Args(profiles, cl_args)
        self.profile = self._args.profile

        self._config = self._read_config_file(
            self._profiles.get_config_file_path(
                self.profile
            )
        )

    def __getitem__(self, key):
        """Allows accessing config dict directly on the instance"""
        return self._config[key]

    @staticmethod
    def _read_config_file(config_filepath: Path) -> dict:
        """Delegates to library to parse profile config file as YAML"""
        try:
            with open(config_filepath, "r") as config_stream:
                return yaml.safe_load(config_stream)
        except IOError:
            raise RuntimeError(
                f"Unable to read config file: {config_filepath}"
            )
        except ParserError:
            raise RuntimeError(
                f"Unable to parse config file: {config_filepath}"
            )

    def extract_config_value(
            self,
            key_chain: Iterable[str],
            validator: Callable[[object], bool],
            mapper: Callable[[object], object],
            requirement_msg: str
    ):
        """Streamlines extraction of keys from config"""
        value = self._config
        key_str = '.'.join(key_chain)
        try:
            for key in key_chain:
                value = value[key]
        except (KeyError, TypeError):
            raise RuntimeError(
                f"Failed to extract config value at key '{key_str}'"
                f" from config file {self.profile.get_file_name()}"
            )
        if not validator(value):
            raise RuntimeError(
                f"Illegal config value at key '{key_str}'"
                f" in config file {self.profile.get_file_name()}"
                f" (must be {requirement_msg})"
            )
        try:
            return mapper(value)
        except Exception:
            raise RuntimeError(
                f"Failed to construct object from value(s) at key '{key_str}'"
                f" in config file {self.profile.get_file_name()}"
                f" (must be {requirement_msg})"
            )
