from laksyt.config.config import Config
from laksyt.config.profiles import Profiles
from laksyt.entities.http.schedule import Schedule, get_schedule
from tests.utilities import create_default_profile_config_file


class TestSchedule:

    def test_get_schedule(self, tmpdir):
        # Given
        create_default_profile_config_file(
            tmpdir,
            '''
checking:
  schedule:
    delay: 5
    timeout: 3
            '''
        )

        # When
        schedule: Schedule = get_schedule(Config(Profiles(config_dir=tmpdir)))

        # Then
        assert schedule.delay == 5
        assert schedule.timeout == 3
