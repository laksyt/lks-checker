from enum import Enum


class Profile(Enum):
    """Represents application's runtime profile

    For every defined profile, a configuration file should be present at
    profiles/app-<profile>.yml, where <profile> stands for the enum's value.
    To add a profile, create both an enum instance and a profile file.
    """

    LOCAL = "local"
    PROD = "prod"

    @classmethod
    def default(cls):
        """This profile is used if none are specified at runtime"""
        return Profile.LOCAL

    def __str__(self):
        """This is strictly for appearance in command line help messages"""
        return self.value
