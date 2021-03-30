import pytest

from laksyt.config.args import Args, PROFILE_ENV_VAR_NAME
from laksyt.config.profiles import Profiles
from tests.utilities import create_test_profiles


class TestArgs:
    """Tests whether runtime args are parsed correctly"""

    def test_default_profile(self, monkeypatch, tmpdir):
        # Given
        create_test_profiles(tmpdir)
        profiles = Profiles(config_dir=tmpdir)
        monkeypatch.delenv(name=PROFILE_ENV_VAR_NAME, raising=False)

        # When
        args = Args(profiles, [])

        # Then
        assert args.profile == profiles.default

    def test_profile_from_env(self, monkeypatch, tmpdir):
        # Given
        create_test_profiles(tmpdir)
        profiles = Profiles(config_dir=tmpdir)
        monkeypatch.setenv(name=PROFILE_ENV_VAR_NAME, value='uat')

        # When
        args = Args(profiles, [])

        # Then
        assert args.profile == profiles.Profile('uat')

    def test_profile_from_cli(self, monkeypatch, tmpdir):
        # Given
        create_test_profiles(tmpdir)
        profiles = Profiles(config_dir=tmpdir)
        monkeypatch.delenv(name=PROFILE_ENV_VAR_NAME, raising=False)

        # When
        args = Args(profiles, ['--profile', 'dev'])

        # Then
        assert args.profile == profiles.Profile('dev')

    def test_profile_from_env_and_cli(self, monkeypatch, tmpdir):
        # Given
        create_test_profiles(tmpdir)
        profiles = Profiles(config_dir=tmpdir)
        monkeypatch.setenv(name=PROFILE_ENV_VAR_NAME, value='uat')

        # When
        args = Args(profiles, ['--profile', 'dev'])

        # Then
        assert args.profile == profiles.Profile('dev')

    def test_bad_profile_from_env(self, monkeypatch, tmpdir):
        with pytest.raises(RuntimeError):
            # Given
            create_test_profiles(tmpdir)
            profiles = Profiles(config_dir=tmpdir)
            monkeypatch.setenv(name=PROFILE_ENV_VAR_NAME, value='mumbo')

            # When
            Args(profiles, [])

            # Then an error is raised due to bad profile name

    def test_bad_profile_from_env_overridden(self, monkeypatch, tmpdir):
        # Given
        create_test_profiles(tmpdir)
        profiles = Profiles(config_dir=tmpdir)
        monkeypatch.setenv(name=PROFILE_ENV_VAR_NAME, value='mumbo')

        # When
        args = Args(profiles, ['--profile', 'dev'])

        # Then
        assert args.profile == profiles.Profile('dev')

    def test_bad_profile_from_cli(self, monkeypatch, tmpdir):
        with pytest.raises(SystemExit):
            # Given
            create_test_profiles(tmpdir)
            profiles = Profiles(config_dir=tmpdir)
            monkeypatch.delenv(name=PROFILE_ENV_VAR_NAME, raising=False)

            # When
            Args(profiles, ['--profile', 'jumbo'])

            # Then an error is raised due to bad profile name

    def test_bad_profile_from_cli_not_overridable(self, monkeypatch, tmpdir):
        with pytest.raises(SystemExit):
            # Given
            create_test_profiles(tmpdir)
            profiles = Profiles(config_dir=tmpdir)
            monkeypatch.setenv(name=PROFILE_ENV_VAR_NAME, value='uat')

            # When
            Args(profiles, ['--profile', 'jumbo'])

            # Then an error is still raised since cli profile cannot be
            # overridden by env var
