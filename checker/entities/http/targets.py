from dataclasses import dataclass
from typing import Optional

from dataclasses_avroschema import AvroModel

from checker.config.config import Config


@dataclass
class Target(AvroModel):
    url: str
    needle: Optional[str] = None


def get_targets(config: Config) -> tuple[Target]:
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
        return tuple(Target(**target_dict) for target_dict in unparsed)
    except (ValueError, TypeError):
        raise RuntimeError(error_msg)
