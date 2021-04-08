from laksyt.config.config import Config
from laksyt.config.profiles import Profiles
from laksyt.entities.target import TargetWrapper, get_targets
from tests.utilities import create_default_profile_config_file


class TestTarget:

    def test_get_targets(self, tmpdir):
        # Given
        create_default_profile_config_file(
            tmpdir,
            '''
checking:
  targets:
    - url: https://nytimes.com
      needle: 'world|peace'
    - url: https://httpstat.us/404
      needle:
            '''
        )

        # When
        targets: tuple[TargetWrapper] = get_targets(
            Config(Profiles(profile_dir=tmpdir))
        )

        # Then
        assert targets is not None
        assert isinstance(targets, tuple)
        assert len(targets) == 2
        assert len([
            target.needle_pattern
            for target in targets
            if target.needle_pattern is not None
        ]) == 1

    def test_get_targets_regex(self, tmpdir):
        # Given
        create_default_profile_config_file(
            tmpdir,
            '''
checking:
  targets:
    - url: https://nytimes.com
      needle: 'world|peace'
            '''
        )
        targets: tuple[TargetWrapper] = get_targets(
            Config(Profiles(profile_dir=tmpdir))
        )
        target, = targets

        # Then
        assert target.needle_is_in('Bye, world!')
        assert not target.needle_is_in('Fools rush in')
