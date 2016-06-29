import base64

def is_base64(s):
    s = ''.join([s.strip() for s in s.split("\n")])
    try:
        enc = base64.b64encode(base64.b64decode(s)).strip()
        return enc == s
    except TypeError:
        return False
