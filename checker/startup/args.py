import argparse
import os
import sys

from checker.startup.profiles import Profiles

PROFILE_ENV_VAR_NAME = 'LAKSYT_PROFILE'


class Args:
    """Parses and stores command line arguments passed to the application

    Accepts overrides from environment. For testability, arguments may be
    passed as a list of strings to the constructor.
    """

    _profiles: Profiles = None
    _parser: argparse.ArgumentParser = None
    _parsed_args: argparse.Namespace = None

    profile = None

    def __init__(
            self,
            profiles: Profiles = Profiles(),
            cl_args: list[str] = None
    ):
        self._profiles = profiles
        self._parser = self._build_parser()
        self._populate_args(self._parser)
        self._parsed_args = self._parse_args(
            self._parser,
            cl_args or sys.argv[1:]
        )
        self.profile = self._get_active_profile()

    @staticmethod
    def _build_parser() -> argparse.ArgumentParser:
        return argparse.ArgumentParser(
            prog="lks-checker",
            description="Python micro-service that performs health-checks"
                        " on a website and reports to a Kafka topic.",
            epilog="Written by Erik Sargazakov.",
            allow_abbrev=True
        )

    def _populate_args(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '-p', '--profile',
            required=False,
            type=self._profiles.Profile,
            help="Name of runtime profile",
            choices=[profile for profile in self._profiles.Profile]
        )

    @staticmethod
    def _parse_args(parser: argparse.ArgumentParser, args: list[str]) \
            -> argparse.Namespace:
        parsed_args, _ = parser.parse_known_args(args)
        return parsed_args

    def _get_active_profile(self):
        return self._parsed_args.profile \
               or self._get_profile_from_env \
               or self._profiles.default

    @property
    def _get_profile_from_env(self):
        env_var_value = os.getenv(PROFILE_ENV_VAR_NAME)
        if env_var_value is not None:
            try:
                return self._profiles.get_by_name(env_var_value)
            except ValueError:
                raise RuntimeError(
                    f"Unrecognized profile '{env_var_value}' given in"
                    f" environment variable {PROFILE_ENV_VAR_NAME}"
                )
        return None
