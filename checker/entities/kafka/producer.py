from kafka import KafkaProducer

from checker.config.config import Config


def get_kafka_producer(config: Config) -> KafkaProducer:
    try:
        kafka_dict: dict = config['kafka']['producer']
    except KeyError:
        raise RuntimeError(
            "Missing key 'kafka.producer'"
            f" in config file {config.profile.get_file_name()}"
        )
    if not kafka_dict:
        raise RuntimeError(
            "Empty key 'kafka.producer'"
            f" in config file {config.profile.get_file_name()}"
        )
    try:
        return KafkaProducer(**kafka_dict)
    except Exception:
        raise RuntimeError(
            "Failed to construct KafkaProducer"
            " from values in key 'kafka.producer'"
            f" in config file {config.profile.get_file_name()}"
        )
