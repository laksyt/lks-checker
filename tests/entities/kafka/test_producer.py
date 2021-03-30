from laksyt.config.config import Config
from laksyt.config.profiles import Profiles
from laksyt.entities.kafka.producer import get_kafka_producer
from tests.utilities import create_default_profile_config_file


class TestKafkaProducer:

    def test_get_kafka_producer(self, tmpdir):
        # Given
        create_default_profile_config_file(
            tmpdir,
            '''
kafka:
  producer:
    bootstrap_servers: non-existing-kafka-server.aivencloud.none:22222
    client_id: lks-checker
    security_protocol: SSL
    ssl_cafile: ca.pem
    ssl_certfile: service.cert
    ssl_keyfile: service.key
            '''
        )

        # When
        get_kafka_producer(
            Config(Profiles(config_dir=tmpdir)),
            handle_kafka_exc=False
        )

        # Then no config parsing errors are raised
