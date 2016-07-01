from flask import current_app, make_response, request, abort, jsonify
import os
from functools import update_wrapper
from clarifai.client import ClarifaiApi
import util
import tempfile


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
        assert app.config['CLIENT_APP_ID'] is not None, 'CLIENT_APP_ID seems to be missing'
        assert app.config['CLIENT_APP_SECRET'] is not None, 'CLIENT_APP_SECRET seems to be missing'
        os.environ['CLARIFAI_APP_ID'] = app.config['CLIENT_APP_ID']
        os.environ['CLARIFAI_APP_SECRET'] = app.config['CLIENT_APP_SECRET']

    @classmethod
    def block(*args, **kwargs):
        def decorator(f):
            def wrapped_function(*args, **kwargs):
                import pdb; pdb.set_trace()
                if request.method == 'POST' or request.method == 'PUT':
                    result = True
                    if request.files:
                        result = NSFW.testFilesAgainstApi(request.files.values())
                    elif request.json:
                        result = NSFW.testBase64Data(request.json.values())
                    if result == False:
                        return jsonify({"response":"seems like the request contains the images that contains nudity."}), 403
                resp = make_response(f(*args, **kwargs))
                return resp
            return update_wrapper(wrapped_function, f)
        return decorator

    @classmethod
    def testFilesAgainstApi(self, data):
        results = clarifai_api.tag_images(data)
        for result in results['results']:
            if result['result']['tag']['classes'][0] == 'nsfw':
                result = result['result']['tag']['probs'][0]
                if result > 0.7:
                    return False
        return True

    @classmethod
    def testBase64Data(self, data):
        files = []
        for d in data:
            f = tempfile.TemporaryFile()
            if util.is_base64(d):
                f.write(d.decode('base64'))
                files.append(f)
        return self.testFilesAgainstApi(files)
