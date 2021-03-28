import os
from enum import Enum
from os import listdir
from os.path import isfile, join

DEFAULT_PROFILE_NAME = 'default'
PROFILE_CONFIG_DIR_PATH = 'profiles'
PROFILE_CONFIG_FILE_NAME_PREFIX = 'app-'
PROFILE_CONFIG_FILE_NAME_SUFFIX = '.yml'
PROJECT_ROOT_DIR = join(os.path.dirname(__file__), os.pardir, os.pardir)


class Profiles:
    """Generates and stores Enum that represents application's runtime profiles

    A profile is defined solely by its YAML configuration file placed at
    profiles/app-<profile>.yml, where <profile> stands for the profile's name.
    To be recognized, profile's name must be a valid Python identifier.

    A profile named 'local' is the default and must always be present.
    """

    config_dir: str = None
    config_file_prefix: str = None
    config_file_suffix: str = None
    Profile = Enum('Profile', {
        DEFAULT_PROFILE_NAME.upper(): DEFAULT_PROFILE_NAME
    })

    def __init__(
            self,
            config_dir: str = join(PROJECT_ROOT_DIR, PROFILE_CONFIG_DIR_PATH),
            config_file_prefix: str = PROFILE_CONFIG_FILE_NAME_PREFIX,
            config_file_suffix: str = PROFILE_CONFIG_FILE_NAME_SUFFIX
    ):
        self.config_dir = config_dir
        self.config_file_prefix = config_file_prefix
        self.config_file_suffix = config_file_suffix
        self.Profile = Enum(
            'Profile',
            {
                profile_name.upper(): profile_name
                for profile_name in self._get_defined_profiles()
            }
        )
        self.Profile.__str__ = lambda item: item.value

    def _get_defined_profiles(self) -> list[str]:
        """Scans profiles directory for YAML config files, ensures the default
        profile is present, returns the full list
        """
        try:
            profile_names = self._scan_dir_for_pattern(
                self.config_dir,
                self.config_file_prefix,
                self.config_file_suffix
            )
        except IOError:
            raise RuntimeError(
                "Failed to read profile config files"
                f" in directory '{PROFILE_CONFIG_DIR_PATH}'"
            )
        if DEFAULT_PROFILE_NAME not in profile_names:
            raise RuntimeError(
                "Failed to detect config file for default profile"
                f" named '{DEFAULT_PROFILE_NAME}'"
            )
        return profile_names

    @staticmethod
    def _scan_dir_for_pattern(dir_path: str, prefix: str, suffix: str) \
            -> list[str]:
        """Scans directory for files named with given prefix & suffix, strips
        both, and returns the remainders of file names in a list
        """
        return [
            filename[len(prefix):len(filename) - len(suffix)]
            for filename in listdir(dir_path)
            if isfile(join(dir_path, filename))
            if len(filename) > len(prefix) + len(suffix)
            if filename.startswith(prefix)
            if filename.endswith(suffix)
        ]

    def get_config_filepath(self, profile: Profile):
        return join(
            self.config_dir,
            f"{self.config_file_prefix}"
            f"{profile.value}"
            f"{self.config_file_suffix}"
        )

    def get_by_name(self, name: str) -> Profile:
        return self.Profile(name)

    @property
    def default(self) -> Profile:
        return self.Profile(DEFAULT_PROFILE_NAME)

    def __call__(self):
        return self.Profile.__call__()

    def __iter__(self):
        return iter(self.Profile)

    def __next__(self):
        return next(self.Profile)

    def __len__(self):
        return len(self.Profile)
