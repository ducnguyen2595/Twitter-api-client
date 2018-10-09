""" Test Twitter Api client"""
import logging
import os

import pytest
from mock import MagicMock, patch
from twitter import *
from twitter_api import client
from werkzeug.exceptions import InternalServerError

mock_logger = logging.getLogger("abc")


class TestTwitterClient():

    @patch.object(OAuth, "__init__", return_value=None)
    def test_correct_token(self, mock_oauth):
        os.environ["TWITTER_ACCESS_KEY"] = "a"
        os.environ["TWITTER_ACCESS_SECRET"] = "b"
        os.environ["TWITTER_CONSUMER_KEY"] = "c"
        os.environ["TWITTER_CONSUMER_SECRET"] = "d"  # export mock keys value

        client.TwitterClient(mock_logger)
        mock_oauth.assert_called_with('a', 'b', 'c', 'd')

    @patch.object(Twitter, "__init__", return_value=None)
    @patch.object(OAuth, "__init__", return_value=None)
    def test_create_correct_object(self, mock_oauth_init, mock_twitter):
        os.environ["TWITTER_ACCESS_KEY"] = "a"
        os.environ["TWITTER_ACCESS_SECRET"] = "b"
        os.environ["TWITTER_CONSUMER_KEY"] = "c"
        os.environ["TWITTER_CONSUMER_SECRET"] = "d"  # export mock keys value

        _ = client.TwitterClient(mock_logger)

        # check if object create with that value
        mock_oauth_init.assert_called_with('a', 'b', 'c', 'd')
        assert mock_twitter.called  # check if object create

    def test_call_parent_get_raise_exception(self):
        """ Verify if raise correct exception
        """
        twitter = client.TwitterClient(mock_logger)
        with pytest.raises(NotImplementedError) as e:
            twitter.get(30)
        assert str(e.value) == "Child class should implement this"


class TestHashtagClient():

    @patch.object(logging.Logger, "info")
    def test_get(self, mock_logging):
        """ test get function call  with correct steps"""
        twitter = client.HashtagClient(mock_logger)
        twitter.client.search.tweets = MagicMock()
        with pytest.raises(TwitterHTTPError) as e:
            twitter.get("abc", 3)

        mock_logging.assert_called_with("Searching Hashtag = #abc")
        assert twitter.client.search.tweets.called


class TestScreenUserClient():

    @patch.object(logging.Logger, "info")
    def test_get(self, mock_logging):
        """ test get function call  with correct steps"""
        twitter = client.ScreenUserClient(mock_logger)
        twitter.client.statuses.user_timeline = MagicMock()
        with pytest.raises(InternalServerError) as e:
            twitter.get("python", 3)

        mock_logging.assert_called_with("Get User TimeLine, name = python")
        assert twitter.client.statuses.user_timeline.called
