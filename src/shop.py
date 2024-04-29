from .app import app
import flask


@app.route("/shop", methods=["GET", "POST"])
def shop():
    if flask.request.method == "GET":
        # stub method for getting list of shops
        raise NotImplementedError
    elif flask.request.method == "POST":
        # stub method for creating a new shop
        raise NotImplementedError
    else:
        return flask.Response(status=405)


@app.route("/shop/<int:shop_id>", methods=["GET", "PUT", "DELETE"])
def shop_id(shop_id):
    if flask.request.method == "GET":
        # stub method for getting a shop by id
        raise NotImplementedError
    elif flask.request.method == "PUT":
        # stub method for updating a shop details by id
        raise NotImplementedError
    elif flask.request.method == "DELETE":
        # stub method for deleting a shop by id
        raise NotImplementedError
    else:
        return flask.Response(status=405)


@app.route("/shop/<int:shop_id>/products", methods=["GET"])
def shop_products(shop_id):
    if flask.request.method == "GET":
        # stub method for getting list of products in a shop
        raise NotImplementedError
    else:
        return flask.Response(status=405)


@app.route(
    "/shop/<int:shop_id>/products/<int:product_id>",
    methods=["GET", "POST", "PUT", "DELETE"],
)
def shop_product_id(shop_id, product_id):
    if flask.request.method == "GET":
        # stub method for getting a product in a shop by id
        raise NotImplementedError
    elif flask.request.method == "POST":
        # stub method for adding a product to a shop by id
        raise NotImplementedError
    elif flask.request.method == "PUT":
        # stub method for updating a product in a shop by id
        raise NotImplementedError
    elif flask.request.method == "DELETE":
        # stub method for deleting a product in a shop by id
        raise NotImplementedError
    else:
        return flask.Response(status=405)
