import flask

app = flask.Flask(__name__)

# have flask ignore slashes
app.url_map.strict_slashes = False
