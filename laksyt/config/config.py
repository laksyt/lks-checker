import os
from os.path import join

import yaml

from laksyt.config.args import Args
from laksyt.config.profiles import Profiles

PROJECT_ROOT_DIR = join(os.path.dirname(__file__), os.pardir, os.pardir)


class Config:
    """Encapsulates configurable parameters of the application

    Extracts the name of current runtime profile, then loads and parses the
    appropriate .yml configuration file.
    """

    _profiles: Profiles = None
    _args: Args = None

    profile = None
    _config: dict = None

    def __init__(
            self,
            profiles: Profiles = Profiles(),
            cl_args: list[str] = None
    ):
        self._profiles = profiles
        self._ensure_config_files_are_present()

        self._args = Args(profiles, cl_args)
        self.profile = self._args.profile

        self._config = self._read_config_file(
            self._profiles.get_config_file_path(
                self.profile
            )
        )

    def __getitem__(self, key):
        return self._config[key]

    def _ensure_config_files_are_present(self):
        profiles_without_config = [
            profile.name
            for profile in self._profiles.Profile
            if not os.path.isfile(self._profiles.get_config_file_path(profile))
        ]
        if profiles_without_config:
            raise RuntimeError(
                "Detected profiles without corresponding configuration files:"
                f" {', '.join(profiles_without_config)}"
            )

    @staticmethod
    def _read_config_file(config_filepath: str) -> dict:
        try:
            with open(config_filepath, "r") as config_stream:
                return yaml.safe_load(config_stream)
        except IOError:
            raise RuntimeError(
                f"Unable to read config file: {config_filepath}"
            )
