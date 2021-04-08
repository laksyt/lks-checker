from laksyt.config.config import Config
from laksyt.config.profiles import Profiles
from laksyt.entities.kafka.topic import get_kafka_topic
from tests.utilities import create_default_profile_config_file


class TestTopic:

    def test_get_topic(self, tmpdir):
        # Given
        create_default_profile_config_file(
            tmpdir,
            '''
kafka:
  topic: test-topic
            '''
        )

        # When
        topic: str = get_kafka_topic(Config(Profiles(profile_dir=tmpdir)))

        # Then
        assert topic == 'test-topic'
