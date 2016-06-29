from flask import current_app, make_response, request,abort
import os
from functools import update_wrapper
from clarifai.client import ClarifaiApi
import util

try:
    from flask import _app_ctx_stack as stack
except:
    from flask import _request_ctx_stack as stack

clarifai_api = ClarifaiApi(model='nsfw-v1.0')

class NSFW(object):
    def __init__(self,app):
        self.app = app
        self.init_app(app)

    def init_app(self,app):
        assert app.config['CLIENT_APP_ID'] is not None, 'CLIENT_APP_ID seems to be missing'
        assert app.config['CLIENT_APP_SECRET'] is not None, 'CLIENT_APP_SECRET seems to be missing'
        os.environ['CLARIFAI_APP_ID'] = app.config['CLIENT_APP_ID']
        os.environ['CLARIFAI_APP_SECRET'] = app.config['CLIENT_APP_SECRET']

    @classmethod
    def block(*args, **kwargs):
        def decorator(f):
            def wrapped_function(*args, **kwargs):
                if request.method == 'POST':
                    if len(request.files.keys()) > 0:
                        for key in request.files:
                            result = clarifai_api.tag_images(request.files[key])
                            if result['results'][0]['result']['tag']['classes'][0] == 'nsfw':
                                result = result['results'][0]['result']['tag']['probs']
                                if result[0] > 0.7:
                                    abort(400)
                    elif request.json is not None:
                        for key in request.json:
                            if util.is_base64(request.json[key]):
                                base64String = request.json[key]
                                file = open('temp.jpg','w+')
                                file.write(base64String.decode('base64'))
                                result = clarifai_api.tag_images(file)
                                file.close()
                            if result['results'][0]['result']['tag']['classes'][0] == 'nsfw':
                                result = result['results'][0]['result']['tag']['probs']
                                if result[0] > 0.7:
                                    abort(400)
                try:
                    os.system('rm temp.jpg')
                except:
                    pass
                # resp = current_app.make_default_options_response()
                resp = make_response(f(*args, **kwargs))
                return resp
            return update_wrapper(wrapped_function, f)
        return decorator
