import flask
from .shop import shop_blueprint
from .products import products_blueprint
from .healthz import healthz_blueprint

app = flask.Flask(__name__)

# have flask ignore slashes
app.url_map.strict_slashes = False

# register the blueprints
app.register_blueprint(shop_blueprint, url_prefix="/shop")
app.register_blueprint(products_blueprint, url_prefix="/products")
app.register_blueprint(healthz_blueprint, url_prefix="/healthz")
