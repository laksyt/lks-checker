from os.path import join

import pytest

from laksyt.config.profiles import DEFAULT_PROFILE_NAME, Profiles
from tests.utilities import create_config_file


class TestProfiles:
    """Tests whether profiles dir is scanned correctly"""

    def test_default_profile_name(self):
        assert DEFAULT_PROFILE_NAME.isidentifier()

    def test_scan_profiles_dir(self, tmpdir):
        # Given
        base = DEFAULT_PROFILE_NAME
        create_config_file(tmpdir, f"app-{base}.yml")
        create_config_file(tmpdir, f"app-{base}1.yml")
        create_config_file(tmpdir, f"app-{base}2.yaml")
        create_config_file(tmpdir, f"app-{base}3.yml")
        create_config_file(tmpdir, f"app-{base}4.yml")
        create_config_file(tmpdir, "app-.yml")
        create_config_file(tmpdir, "some_other_file")
        expected = (
            base, f"{base}1", f"{base}3", f"{base}4"
        )

        # When
        actual = Profiles(tmpdir, 'app-', '.yml')

        # Then
        assert len(actual) == len(expected)
        assert {profile.value for profile in actual} == set(expected)

    def test_scan_empty_profiles_dir(self, tmpdir):
        with pytest.raises(RuntimeError):
            # When
            Profiles(tmpdir, 'app-', '.yml')

            # Then an error is raised because default profile is missing

    def test_scan_missing_profiles_dir(self, tmpdir):
        with pytest.raises(RuntimeError):
            # When
            Profiles(f"{tmpdir}-non-existing", 'app-', '.yml')

            # Then an error is raised because dir is inaccessible

    def test_get_by_name(self, tmpdir):
        # Given
        create_config_file(tmpdir, f"app-{DEFAULT_PROFILE_NAME}.yml")
        create_config_file(tmpdir, "app-profile1.yml")
        profiles = Profiles(tmpdir, 'app-', '.yml')

        # When
        actual = profiles.get_by_name('profile1')

        # Then
        assert actual.value == 'profile1'
        assert actual.name == 'PROFILE1'

    def test_get_config_filepath(self, tmpdir):
        # Given
        test_file_name = "app-profile_name.yml"
        create_config_file(tmpdir, f"app-{DEFAULT_PROFILE_NAME}.yml")
        create_config_file(tmpdir, test_file_name)
        profiles = Profiles(tmpdir, 'app-', '.yml')
        profile = profiles.get_by_name('profile_name')

        # When
        actual = profiles.get_config_file_path(profile)

        # Then
        assert actual == join(tmpdir, test_file_name)
