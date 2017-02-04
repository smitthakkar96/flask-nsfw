"""
All the crazy utilites are present here
"""


import base64
import binascii
import re


def is_base64(string):
    """
        Checks wether the given string is base64 or not
    """
    try:
        base64.decodestring(str.encode(string))
        return True
    except binascii.Error:
        return False

def is_url(string):
    """
        Used to check wether the given string is url or not
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE)
    url = regex.match(string)
    if url:
        return True
    return False


class InvalidUsage(Exception):
    """
        A custom Exception to trigger errors like 401, 400 etc
    """
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """
            creates a dict containing an error message which is later converted to json
        """
        error = dict(self.payload or ())
        error['message'] = self.message
        return error

