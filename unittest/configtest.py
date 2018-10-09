import pytest
from mock import MagicMock, patch

from twitter_gateway.app import app as twitter_gateway
from twitter_api.client import HashtagClient, ScreenUserClient

@pytest.fixture
def app():
    return twitter_gateway

@pytest.fixture
@patch.object(HashtagClient, "get", return_value={"foo": "bar"})
def mock_hashtag_client(mock_hashtag_client):
    return mock_hashtag_client