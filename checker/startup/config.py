import os

import yaml

from checker.startup import args
from checker.startup.profile import Profile


class Config:
    """Encapsulates configurable parameters of the application

    Extracts the name of current runtime profile, then loads and parses the
    appropriate .yml configuration file.
    """

    _args: args.Args = None
    profile: Profile = None

    _config_filepath: str = None
    _config: dict = None

    def __init__(self, cl_args: list[str] = None):
        self._ensure_config_files_are_present()

        self._args = args.Args(cl_args)
        self.profile = self._args.profile

        self._config_filepath = self._get_config_filepath(self.profile)
        self._config = self._read_config_file(self._config_filepath)

    def __getitem__(self, key):
        return self._config[key]

    @staticmethod
    def _read_config_file(config_filepath: str) -> dict:
        try:
            with open(config_filepath, "r") as config_stream:
                return yaml.safe_load(config_stream)
        except IOError:
            raise RuntimeError(
                f"Unable to read config file: {config_filepath}"
            )

    @staticmethod
    def _ensure_config_files_are_present():
        profiles_without_config = [
            profile.name
            for profile in Profile
            if not os.path.isfile(Config._get_config_filepath(profile))
        ]
        if profiles_without_config:
            raise RuntimeError(
                "Detected profiles without corresponding configuration files:"
                f" {', '.join(profiles_without_config)}"
            )

    @staticmethod
    def _get_config_filepath(profile: Profile) -> str:
        return f"profiles/app-{profile.value}.yml"
