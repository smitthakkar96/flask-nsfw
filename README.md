# flask-nsfw
While build the apps that serve users sometimes you are concern with the type of content sent to server. 
Sometimes there are some images sent to server that contains nudity etc, in such cases you look forward for some rest API and then call it in each function.

But now those old days are gone, here is flask-nsfw a simple flask extension built with Clarifai Api. Just add a decorate before function and there you go.
Currently flask-nsfw block images that are in form of multipart or base64.

To use flask-nsfw : 
step 1: pip install flask-nsfw
step 2: create account on clarifai
step 3: Follow the example below.

```

from flask import Flask
from flask_nsfw import flask_nsfw

app = Flask(__name__)

app.config['CLIENT_APP_ID'] = 'xdObb0J7roCo_an5ahhezJrHyds_vfdHk35kzWyB'
app.config['CLIENT_APP_SECRET'] = 'UEovD-ppGwmhEXz7HBPdZBjT7iDslcisIl_M2qK7'


nsfw = flask_nsfw(app)

@app.route('/',methods=['POST'])
@nsfw.block_nsfw()
def index():
    return "Request contains no NSFW content"

if __name__ == '__main__':
    app.run(debug=True)


```

