"""
    The logic to block all the crazy NSFW content coming to your rest apis is present here.
"""

import os
import tempfile
from functools import wraps
import base64

from flask import request, jsonify
from clarifai.client import ClarifaiApi

import util

try:
    from flask import _app_ctx_stack as stack
except:
    from flask import _request_ctx_stack as stack

clarifai_api = ClarifaiApi(model='nsfw-v1.0')


class NSFW(object):

    def __init__(self, app):
        self.app = app
        self.init_app(app)

    def init_app(self, app):
        """
            Initilize the stuff
        """
        assert app.config['CLIENT_APP_ID'] is not None, 'CLIENT_APP_ID seems to be missing'
        assert app.config['CLIENT_APP_SECRET'] is not None, 'CLIENT_APP_SECRET seems to be missing'
        os.environ['CLARIFAI_APP_ID'] = app.config['CLIENT_APP_ID']
        os.environ['CLARIFAI_APP_SECRET'] = app.config['CLIENT_APP_SECRET']

    def block(self):
        """
            block is a decorator function that wraps around the route and does all the crazy stuff
        """
        def decorator(func):
            @wraps(func)
            def wrapped():
                if request.method == 'POST' or request.method == 'PUT':
                    result = True
                    result2 = True
                    if request.form:
                        result2 = self.collect_urls(request.form.values())
                    if request.files:
                        result = self.test_files_against_api(
                            request.files.values())
                    elif request.json:
                        result = self.test_base64_data(request.json.values())
                        result2 = self.collect_urls(request.json.values())
                    if not result or not result2:
                        return jsonify({"response": "seems like the request contains the" \
                                        + " images that contains NSFW content."}), 403
                return func()
            return wrapped
        return decorator

    @classmethod
    def test_urls_against_api(cls, urls):
        """
            This Method will test urls and return nsfw evalation
        """
        if "CLARIFAI_APP_ID" in os.environ:
            results = clarifai_api.tag_urls(urls)
            for result in results['results']:
                if result['result']['tag']['classes'][0] == 'nsfw':
                    result = result['result']['tag']['probs'][0]
                    if result > 0.7:
                        return False
            return True
        else:
            return Exception("Please set ClarifaiApi credentials")

    @classmethod
    def test_files_against_api(cls, data):
        """
            This Method will test file objects and return nsfw evalation
        """
        if "CLARIFAI_APP_ID" in os.environ:
            results = clarifai_api.tag_images([d for d in data])
            for result in results['results']:
                if result['result']['tag']['classes'][0] == 'nsfw':
                    result = result['result']['tag']['probs'][0]
                    if result > 0.7:
                        return False
            return True
        else:
            return Exception("Please set ClarifaiApi credentials")


    @classmethod
    def collect_urls(cls, data):
        """
            This Method will collect all the urls from given string
        """
        urls = []
        for string in data:
            if util.is_url(string):
                urls.append(string)
        return cls.test_urls_against_api(urls)


    @classmethod
    def test_base64_data(cls, data):
        """
            This Method will test base64 data and return nsfw evalation
        """
        files = []
        for file_obj in data:
            image_file = tempfile.NamedTemporaryFile("wb+")
            if util.is_base64(file_obj):
                image_file.write(base64.decodestring(str.encode(file_obj)))
                image_file.seek(0, 0)
                files.append(image_file)
        return cls.test_files_against_api(files)
