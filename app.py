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
