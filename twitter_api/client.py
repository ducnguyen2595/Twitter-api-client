import os
import requests
import logging
import base64
from twitter import *
from flask import jsonify, abort

class TwitterClient():
    def __init__(self, logger):
        self.logger = logger
        ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_KEY")
        ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")
        CONSUMER_TOKEN = os.environ.get("TWITTER_CONSUMER_KEY")
        CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
        self.client = Twitter(auth=OAuth(ACCESS_TOKEN,
                                         ACCESS_SECRET,
                                         CONSUMER_TOKEN,
                                         CONSUMER_SECRET,
        ))
    def get(self, limit):
        raise NotImplementedError("Child class should implement this")

class HashtagClient(TwitterClient):
    def __init__(self, logger):
        super().__init__( logger)

    def get(self, query, limit):
        self.logger.info(f"Searching Hashtag = #{query}")
        result = self.client.search.tweets(q=f"#{query}", count=limit)
        return result

class ScreenUserClient(TwitterClient):

    def get(self, query, limit):
        self.logger.info(f"Get User TimeLine, name = {query}")
        try:
            result = self.client.statuses.user_timeline(screen_name=query, count=limit)
            return result
        except TwitterHTTPError as E:
            if "not exist" in str(E):
                self.logger.debug(f"abcbcbcb: {str(E)}")
                abort(404, f"User {query} doesn't exist", )
            else:
                self.log.error(f"Failed to screen user {query}, exception: {str(E)}")
                abort(500, "Internal server Error")
