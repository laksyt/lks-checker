from laksyt.config.config import Config
from laksyt.config.profiles import DEFAULT_PROFILE_NAME, Profiles
from tests.startup.utilities import create_profile_config_file


class TestConfig:
    def test_config(self, tmpdir):
        # When
        config = Config()

        # Then
        assert config.profile.value == DEFAULT_PROFILE_NAME
        assert config.profile.name == DEFAULT_PROFILE_NAME.upper()

    def test_config_content(self, tmpdir):
        # Given
        create_profile_config_file(
            tmpdir,
            DEFAULT_PROFILE_NAME,
            'key: value'
        )

        # When
        config = Config(Profiles(config_dir=tmpdir))

        # Then
        assert config['key'] == 'value'

    def test_config_nested_content(self, tmpdir):
        # Given
        create_profile_config_file(
            tmpdir,
            DEFAULT_PROFILE_NAME,
            'key:\n  sub: value'
        )

        # When
        config = Config(Profiles(config_dir=tmpdir))

        # Then
        assert config['key']['sub'] == 'value'

    def test_config_chained_content(self, tmpdir):
        # Given
        create_profile_config_file(
            tmpdir,
            DEFAULT_PROFILE_NAME,
            'key.sub: value'
        )

        # When
        config = Config(Profiles(config_dir=tmpdir))

        # Then
        assert config['key.sub'] == 'value'
