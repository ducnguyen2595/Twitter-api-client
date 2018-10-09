import os

import requests

import pytest
from configtest import app, mock_hashtag_client
from flask import url_for
from mock import MagicMock, patch
from twitter import *
from twitter_gateway.app import HashtagResource, UserTimelineResource


class TestApp:

    def test_index(self, client):
        help_text = "Welcome To Twitter Gateway! Currently We support two " \
                    "apis: /hashtags/{tag}: To get list of tweets with the #tag\n" \
                    "/users/{name}: To Get list of tweets on user {name}'s feet\n" \
                    "limit: optional parameter, number of tweet to retrieve, " \
                    "maximum is 200, default 30 \n"
        res = client.get(url_for('index'))
        assert res.status_code==200
        assert res.json == help_text
