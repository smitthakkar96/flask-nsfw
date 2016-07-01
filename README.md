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

<hr/>

<b>TODOS</b><br>
1.Follow pep8 <br/>
2. add support for put method - Done <br/>
3. temp file (windows,linux) also developer can override it. - partly done <br/>
4. separate the code that deals with api - Done <br/>
5. Response 403, add reason too with file name and field name. - Done <br/>
6. fix line no 37 remove none check - Done <br/>
7. Developer docs later - Not now <br/>
8. Convert to python3  <br/>
9. file type encoding  <br/>
