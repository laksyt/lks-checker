import argparse
import os
import sys
from typing import Optional

from checker.startup.profile import Profile


class Args:
    """Parses and stores command line arguments passed to the application

    Accepts overrides from environment. For testability, arguments may be
    passed as a list of strings to the constructor.
    """

    PROFILE_ENV_VAR_NAME = 'LAKSYT_ENV'

    _parser: argparse.ArgumentParser = None
    _parsed_args: argparse.Namespace = None

    def __init__(self, cl_args: list[str] = None):
        self._parser = self._build_parser()
        self._populate_args(self._parser)
        self._parsed_args = self._parse_args(
            self._parser,
            cl_args or sys.argv[1:]
        )

    @staticmethod
    def _build_parser() -> argparse.ArgumentParser:
        return argparse.ArgumentParser(
            prog="lks-checker",
            description="Python micro-service that performs health-checks"
                        " on a website and reports to a Kafka topic.",
            epilog="Written by Erik Sargazakov.",
            allow_abbrev=True
        )

    @staticmethod
    def _populate_args(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '-p', '--profile',
            required=False,
            type=Profile,
            help="Name of runtime profile",
            choices=[profile for profile in Profile]
        )

    @staticmethod
    def _parse_args(parser: argparse.ArgumentParser, args: list[str]) \
            -> argparse.Namespace:
        parsed_args, _ = parser.parse_known_args(args)
        return parsed_args

    @property
    def profile(self) -> Profile:
        return self._parsed_args.profile \
               or self._profile_from_env \
               or Profile.default()

    @property
    def _profile_from_env(self) -> Optional[Profile]:
        env_var_value = os.getenv(Args.PROFILE_ENV_VAR_NAME)
        if env_var_value is not None:
            try:
                return Profile(env_var_value)
            except ValueError:
                raise RuntimeError(
                    f"Unrecognized profile '{env_var_value}' given in"
                    f" environment variable {Args.PROFILE_ENV_VAR_NAME}"
                )
        return None
