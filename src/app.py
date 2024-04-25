import flask

app = flask.Flask(__name__)

# have flask ignore slashes
app.url_map.strict_slashes = False

#make a healthz route
@app.route('/healthz')
def healthz():
    return 'ok'

#make a hello home route
@app.route('/')
def hello():
    return 'Hello, World!'
