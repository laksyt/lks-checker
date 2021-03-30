"""Extracts and validates Kafka producer parameters from the application config
file for the active profile, then constructs and returns the producer object
"""

from kafka import KafkaProducer

from laksyt.config.config import Config


def get_kafka_producer(config: Config) -> KafkaProducer:
    return config.extract_config_value(
        ('kafka', 'producer'),
        lambda x: x is not None and isinstance(x, dict),
        lambda x: KafkaProducer(**x),
        "dict with fields for KafkaProducer constructor"
    )
