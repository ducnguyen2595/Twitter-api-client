""" This file contains helper functions
"""
from flask import jsonify
import requests
def header_only_accept(key, header):
    """ check if header accept `key` data type"""
    return key in header['Accept']

def make_response(request_header, response_for_client):
    if header_only_accept("application/json", request_header):
        response_for_client = jsonify(response_for_client)
        response_for_client["header"] = "'Content-Type': 'application/json'"
    return response_for_client
