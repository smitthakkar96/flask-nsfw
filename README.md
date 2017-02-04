# Flask-NSFW
Flask-NSFW is a wrapper around clarifai api that helps to prenvent the NSFW content coming to your flask backend.

Currently flask-nsfw blocks images that are sents as multipart, base64 or url.<br/>

[![Build Status](https://travis-ci.org/smitthakkar96/flask-nsfw.svg?branch=master)](https://travis-ci.org/smitthakkar96/flask-nsfw)
[![PyPI version](https://badge.fury.io/py/Flask-NSFW.svg)](https://badge.fury.io/py/Flask-NSFW)

To use flask-nsfw :
Step 1: Run `pip install flask-nsfw` [(link here)](https://pypi.python.org/pypi/Flask-NSFW/1.0) <br/>
Step 2: Create account on [Clarifai](http://developer.clarifai.com) <br/>
Step 3: Follow the example below. <br/>

```

from flask import Flask
from flask_nsfw import NSFW

app = Flask(__name__)

app.config['CLIENT_APP_ID'] = '<Clarifai App ID>'
app.config['CLIENT_APP_SECRET'] = 'Clarifai App Secret'


nsfw = NSFW(app)

@app.route('/',methods=['POST'])
@nsfw.block()
def index():
    return "Request contains no NSFW content"

if __name__ == '__main__':
    app.run(debug=True)
```
