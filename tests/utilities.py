import os

from laksyt.config.profiles import DEFAULT_PROFILE_NAME, PROFILE_CONFIG_FILE_NAME_PREFIX, \
    PROFILE_CONFIG_FILE_NAME_SUFFIX


def create_config_file(dir_path: str, file_name: str, content=None):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'w') as file:
        file.write(content or 'key: value')


def create_profile_config_file(dir_path: str, profile_name: str, content=None):
    create_config_file(
        dir_path,
        f"{PROFILE_CONFIG_FILE_NAME_PREFIX}"
        f"{profile_name}"
        f"{PROFILE_CONFIG_FILE_NAME_SUFFIX}",
        content
    )


def create_default_profile_config_file(dir_path: str, content=None):
    create_config_file(
        dir_path,
        f"{PROFILE_CONFIG_FILE_NAME_PREFIX}"
        f"{DEFAULT_PROFILE_NAME}"
        f"{PROFILE_CONFIG_FILE_NAME_SUFFIX}",
        content
    )


def create_test_profiles(dir_path: str):
    create_profile_config_file(dir_path, DEFAULT_PROFILE_NAME)
    create_profile_config_file(dir_path, 'prod')
    create_profile_config_file(dir_path, 'dev')
    create_profile_config_file(dir_path, 'uat')
