"""Configures application logging (duh)"""

import logging
import sys

from laksyt.config.config import Config

LOG_FORMAT = '%(asctime)s.%(msecs)03d %(levelname)8.8s %(process)5s' \
             ' --- [%(threadName)15.15s] %(name)-24.24s: %(message)s'
LOF_DATEFMT = '%Y-%m-%d %H:%M:%S'


def configure_logging(config: Config):
    log_level = config.extract_config_value(
        ('log', 'level'),
        lambda x: x is not None and isinstance(x, str) and x in (
            'CRITICAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET'
        ),
        lambda x: x,
        'any of: CRITICAL, ERROR, WARNING, WARN, INFO, DEBUG, NOTSET'
    )

    logging.basicConfig(
        format=LOG_FORMAT,
        level=logging.getLevelName(log_level),
        datefmt=LOF_DATEFMT,
        stream=sys.stderr
    )
