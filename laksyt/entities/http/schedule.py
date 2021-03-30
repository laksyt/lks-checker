"""Defines an abstraction for storing scheduling configuration

delay (int): Duration in seconds between the end of a round of health checks
    and the beginning of the next one.
timeout (int): Duration in seconds to wait for a response from a website before
    considering it unavailable.
"""

from collections import namedtuple

from laksyt.config.config import Config

Schedule = namedtuple('Schedule', ['delay', 'timeout'])


def get_schedule(config: Config) -> Schedule:
    """Extracts and validates scheduling parameters from the application config
    file for the active profile
    """
    checking_delay = config.extract_config_value(
        ('checking', 'schedule', 'delay'),
        lambda x: x is not None and isinstance(x, int) and 5 <= x <= 3600,
        lambda x: x,
        'int in range [5,3600]'
    )
    checking_timeout = config.extract_config_value(
        ('checking', 'schedule', 'timeout'),
        lambda x: x is not None and isinstance(x, int) and 0 < x <= 60,
        lambda x: x,
        'int in range (0,60]'
    )
    return Schedule(
        delay=checking_delay,
        timeout=checking_timeout
    )
