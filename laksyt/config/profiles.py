from enum import Enum
from os import listdir
from pathlib import Path

DEFAULT_PROFILE_NAME = 'default'
PROFILE_DIR_NAME = 'profiles'
PROFILE_FILE_NAME_PREFIX = 'app-'
PROFILE_FILE_NAME_SUFFIX = '.yml'
PROJECT_ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
CURRENT_WORK_DIR = Path.cwd().resolve()


class Profiles:
    """Generates and stores Enum that represents application's runtime profiles

    A profile is defined solely by its YAML configuration file placed at
    profiles/app-<profile>.yml, where <profile> stands for the profile's name.
    To be recognized, profile's name must be a valid Python identifier.

    Default profile (name defined at the top of this script) must always be
    present.
    """

    def __init__(
            self,
            profile_dir: str = None,
            profile_file_name_prefix: str = PROFILE_FILE_NAME_PREFIX,
            profile_file_name_suffix: str = PROFILE_FILE_NAME_SUFFIX
    ):
        self.profile_dir = self._detect_profile_dir(profile_dir)
        self.profile_file_name_prefix = profile_file_name_prefix
        self.profile_file_name_suffix = profile_file_name_suffix
        self.Profile = self._generate_profile_enum()

    @staticmethod
    def _detect_profile_dir(explicit: str = None) -> Path:
        """Decides where to look for profile config files"""
        if explicit is not None:
            explicit = Path(explicit)
            if explicit.is_dir():
                return explicit
            raise RuntimeError(
                f"Explicitly given config directory {explicit} does not exist"
            )
        in_cwd = CURRENT_WORK_DIR.joinpath(PROFILE_DIR_NAME)
        if in_cwd.is_dir():
            return in_cwd
        in_root = PROJECT_ROOT_DIR.joinpath(PROFILE_DIR_NAME)
        if in_root.is_dir():
            return in_root
        raise RuntimeError(
            "Failed to detect config directory at following locations:"
            f" {', '.join({str(in_cwd), str(in_root)})}"
        )

    def _generate_profile_enum(self) -> Enum:
        """Generates Profile enum and adds convenience methods to it"""
        enum = Enum(
            'Profile',
            {
                profile_name.upper(): profile_name
                for profile_name in self._get_defined_profiles()
            }
        )
        enum.get_file_name = lambda p: self.get_config_file_name(p)
        enum.get_file_path = lambda p: self.get_config_file_path(p)
        enum.__str__ = lambda item: item.value
        return enum

    def _get_defined_profiles(self) -> list[str]:
        """Scans profiles directory for YAML config files, ensures the default
        profile is present, returns the full list
        """
        try:
            profile_names = [
                profile_name
                for profile_name in self._scan_dir_for_pattern(
                    self.profile_dir,
                    self.profile_file_name_prefix,
                    self.profile_file_name_suffix
                ) if profile_name.isidentifier()
            ]
        except IOError:
            raise RuntimeError(
                f"Failed to read profile config files in {self.profile_dir}"
            )
        if DEFAULT_PROFILE_NAME not in profile_names:
            raise RuntimeError(
                "Failed to detect config file for default profile"
                f" '{DEFAULT_PROFILE_NAME}' in {self.profile_dir}"
            )
        return profile_names

    @staticmethod
    def _scan_dir_for_pattern(dir_path: Path, prefix: str, suffix: str) \
            -> list[str]:
        """Scans directory for files named with given prefix & suffix, strips
        both, and returns the remainders of file names in a list
        """
        return [
            filename[len(prefix):len(filename) - len(suffix)]
            for filename in listdir(dir_path)
            if dir_path.joinpath(filename).is_file()
            if len(filename) > len(prefix) + len(suffix)
            if filename.startswith(prefix)
            if filename.endswith(suffix)
        ]

    def get_config_file_name(self, profile):
        return f"{self.profile_file_name_prefix}" \
               f"{profile.value}" \
               f"{self.profile_file_name_suffix}"

    def get_config_file_path(self, profile) -> Path:
        return self.profile_dir.joinpath(self.get_config_file_name(profile))

    def get_by_name(self, name: str):
        return self.Profile(name)

    @property
    def default(self):
        return self.Profile(DEFAULT_PROFILE_NAME)

    def __call__(self):
        return self.Profile.__call__()

    def __iter__(self):
        return iter(self.Profile)

    def __next__(self):
        return next(self.Profile)

    def __len__(self):
        return len(self.Profile)
