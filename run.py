import os
import pytest


config = {
    'REMOTE_IP': '127.0.0.1'
}


def set_envs(envs_config: dict):
    for env in envs_config:
        if not os.getenv(env):
            os.environ[env] = envs_config[env]


def run_all_tests():
    set_envs(config)
    pytest.main([f"-n=5", "-v", "tests", "--alluredir=reports"])


if __name__ == "__main__":
    run_all_tests()
