from json import dumps

from flask import Flask, Response, jsonify, request
from flask_restful import Api, Resource
from twitter_api.client import HashtagClient, ScreenUserClient
from utils import util

app = Flask(__name__)
api = Api(app)


@app.route("/", methods=['GET'])
def index():
    """ index page"""
    help_text = "Welcome To Twitter Gateway! Currently We support two " \
                "apis: /hashtags/{tag}: To get list of tweets with the #tag\n"\
                "/users/{name}: To Get list of tweets on user {name}'s feet\n"\
                "limit: optional parameter, number of tweet to retrieve, " \
                "maximum is 200, default 30 \n"
    return jsonify(help_text)


class HashtagResource(Resource):
    def get(self, tag):

        limit = request.args.get("limit", 30)
        client = HashtagClient(app.logger)
        response = client.get(tag, limit)
        return util.make_response(request.headers, response)

class UserTimelineResource(Resource):
    def get(self, user):

        limit = request.args.get("limit", 30)
        client = ScreenUserClient(app.logger)
        response = client.get(user, limit)
        return util.make_response(request.headers, response)


api.add_resource(HashtagResource, '/hashtags/<tag>')
api.add_resource(UserTimelineResource, '/users/<user>')
