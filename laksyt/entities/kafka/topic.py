"""Extracts and validates name of Kafka topic to post health reports into"""

from laksyt.config.config import Config


def get_kafka_topic(config: Config) -> str:
    return config.extract_config_value(
        ('kafka', 'topic'),
        lambda x: x is not None and isinstance(x, str),
        lambda x: x,
        'str'
    )
