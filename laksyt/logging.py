"""Configures application logging (duh)"""

import logging
import sys

from laksyt.config.config import Config

LOG_FORMAT = '%(asctime)s.%(msecs)03d %(levelname)8.8s %(process)5s' \
             ' --- [%(threadName)15.15s] %(name)-24.24s: %(message)s'
LOF_DATEFMT = '%Y-%m-%d %H:%M:%S'


def configure_logging(config: Config):
    log_level = logging.getLevelName(_get_log_config(config, 'level'))

    if str(log_level).startswith('Level '):
        raise RuntimeError(
            f"Unrecognized log level '{_get_log_config(config, 'level')}'"
            f" in config file {config.profile.get_file_name()}"
        )

    logging.basicConfig(
        format=LOG_FORMAT,
        level=log_level,
        datefmt=LOF_DATEFMT,
        stream=sys.stderr
    )


def _get_log_config(config: Config, key: str):
    try:
        return config['log'][key]
    except KeyError:
        raise RuntimeError(
            f"Unable to find config key 'log.{key}'"
            f" in config file {config.profile.file_path}"
        )
