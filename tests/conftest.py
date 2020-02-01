import configparser

import pytest


@pytest.fixture()
def test_config_path():
    return './tests/samples/test_config.ini'


@pytest.fixture()
def test_config(test_config_path):
    cfg = configparser.ConfigParser()
    cfg.read(test_config_path)
    return cfg
