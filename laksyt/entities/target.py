"""Abstraction for health check target, to be reconstructed from Avro messages
polled from Kafka topic. SQL query template is defined here to be used for
persisting the instances in a PostgreSQL database.

url (str): URL to send a GET request to.
needle (str): Unparsed regex pattern to search for in the HTML content returned
    from the website.
"""

import re
from dataclasses import dataclass
from re import Pattern
from typing import Optional

from dataclasses_avroschema import AvroModel

from laksyt.config.config import Config


@dataclass
class Target(AvroModel):
    url: str
    needle: Optional[str] = None


@dataclass
class TargetWrapper:
    """Wrapper around Target that allows to separate the serialized part from
    the compiled regex pattern for needle"""
    target: Target
    needle_pattern: Optional[Pattern]

    def needle_is_in(self, text: str) -> Optional[bool]:
        """Searches for pre-compiled regex pattern for needle in given text"""
        if not self.needle_pattern:
            return None
        return self.needle_pattern.search(text) is not None


def get_targets(config: Config) -> tuple[TargetWrapper]:
    """Extracts and validates health check targets from config file for active
    profile
    """
    unparsed = config.extract_config_value(
        ('checking', 'targets'),
        lambda x: x is not None and isinstance(x, list),
        lambda x: x,
        "list of 'url'/'needle' pairs ('needle' optional)"
    )
    error_msg = "Key 'checking.targets'" \
                " is not an array of 'url'/'needle' pairs" \
                f" in config file {config.profile.get_file_name()}"
    if not isinstance(unparsed, list) \
            or any(not isinstance(elem, dict) for elem in unparsed):
        raise RuntimeError(error_msg)
    try:
        targets = tuple(Target(**target_dict) for target_dict in unparsed)
    except (ValueError, TypeError):
        raise RuntimeError(error_msg)
    target_wrappers = []
    for target in targets:
        if target.needle is None \
                or not isinstance(target.needle, str) \
                or target.needle.isspace() \
                or target.needle == '':
            target.needle = None
        try:
            target_wrappers.append(TargetWrapper(
                target, re.compile(target.needle) if target.needle else None
            ))
        except re.error:
            raise RuntimeError(
                f"Invalid regular expression '{target.needle}'"
                f" for target URL {target.url}"
            )
    return tuple(target_wrappers)
