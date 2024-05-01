import flask
from flask import Blueprint
from .firestore_db import firestore_db

products_blueprint = Blueprint("products", __name__)


@products_blueprint.route("/", methods=["GET", "POST"])
def products():
    if flask.request.method == "GET":
        # stub method for getting list of products on the platform
        raise NotImplementedError
    elif flask.request.method == "POST":
        # stub method for creating a new product on the platform
        raise NotImplementedError
    else:
        return flask.Response(status=405)


@products_blueprint.route("/<int:product_id>", methods=["GET", "PUT", "DELETE"])
def product_id(product_id):
    if flask.request.method == "GET":
        # stub method for getting a product by id
        raise NotImplementedError
    elif flask.request.method == "PUT":
        # stub method for updating a product details by id
        raise NotImplementedError
    elif flask.request.method == "DELETE":
        # stub method for deleting a product by id
        raise NotImplementedError
    else:
        return flask.Response(status=405)
