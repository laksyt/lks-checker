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
    target: Target
    needle_pattern: Optional[Pattern]

    def needle_is_in(self, text: str) -> Optional[bool]:
        if not self.needle_pattern:
            return None
        return self.needle_pattern.search(text) is not None


def get_targets(config: Config) -> tuple[TargetWrapper]:
    try:
        unparsed = config['checking']['targets']
    except KeyError:
        raise RuntimeError(
            "Missing key 'checking.targets'"
            f" in config file {config.profile.get_file_name()}"
        )
    if not unparsed:
        raise RuntimeError(
            "Empty key 'checking.targets'"
            f" in config file {config.profile.get_file_name()}"
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
