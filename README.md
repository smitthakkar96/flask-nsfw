# flask-nsfw
While building applications that serve users, you may be concerned with the type of content being sent to the server. 
There may be some images sent to the server that contain pornography, nudity etc. In such case you'll have to find a rest API and then call it in every function.

Those old days are gone, here is flask-nsfw a simple flask extension built with Clarifai Api. <br/>
Just add a decorater before the function and you're done.<br/>
Currently flask-nsfw blocks images that are in the form of multipart or base64.<br/>

To use flask-nsfw : 
step 1: pip install flask-nsfw <br/>
step 2: create account on clarifai <br/>
step 3: Follow the example below. <br/>

```

from flask import Flask
from flask_nsfw import NSFW

app = Flask(__name__)

app.config['CLIENT_APP_ID'] = '<Calrifai App ID>'
app.config['CLIENT_APP_SECRET'] = 'Clarifai App Secret'


nsfw = NSFW(app)

@app.route('/',methods=['POST'])
@nsfw.block()
def index():
    return "Request contains no NSFW content"

if __name__ == '__main__':
    app.run(debug=True)


```

