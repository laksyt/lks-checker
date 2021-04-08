"""Application entrypoint

Detects defined runtime profiles, parses configuration file for active (or
default) profile, bootstraps the application, and launches the main workload.
"""

from laksyt.application import Application
from laksyt.config.config import Config
from laksyt.config.profiles import Profiles


def main():
    Application(Config(Profiles())).launch()


if __name__ == "__main__":
    main()
