import base64

def is_base64(s):
    s = ''.join([s.strip() for s in s.split("\n")])
    try:
        enc = base64.b64encode(base64.b64decode(s)).strip()
        return enc == s
    except TypeError:
        return False

from flask import jsonify

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
