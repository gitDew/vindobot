import pytest
import unittest
from credentials import MyCredentials
from unittest.mock import patch, MagicMock


@pytest.fixture
def mocked_credentials():
    credentials = {
            'url': "http://example.com",
            'username': "john",
            'password': "hunter123"
            }
    
    patched_open = patch("builtins.open", MagicMock())

    m = MagicMock(side_effect = [credentials])
    patched_load = patch("json.load", m)

    with patched_open as p_open:
        with patched_load as p_load:
            yield MyCredentials()

def test_get_credentials(mocked_credentials):
    credentials = {
            'url': "http://example.com",
            'username': "john",
            'password': "hunter123"
            }

    assert credentials == mocked_credentials.get_credentials()

def test_memoization(mocked_credentials):
    assert not mocked_credentials.credentials
    mocked_credentials.get_credentials()
    assert mocked_credentials.credentials

def test_idempotency(mocked_credentials):
    c1 = mocked_credentials.get_credentials()
    assert mocked_credentials.credentials

    c2 = mocked_credentials.get_credentials()
    assert c1 == c2




