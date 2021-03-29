from laksyt.config.config import Config


def get_kafka_topic(config: Config) -> str:
    try:
        topic = config['kafka']['topic']
    except KeyError:
        raise RuntimeError(
            "Missing key 'kafka.topic'"
            f" in config file {config.profile.get_file_name()}"
        )
    if not isinstance(topic, str):
        raise RuntimeError(
            "Key 'kafka.topic' should be string"
            f" in config file {config.profile.get_file_name()}"
        )
    return topic
