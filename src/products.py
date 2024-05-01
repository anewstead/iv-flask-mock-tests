import flask
from flask import Blueprint
from .firestore_db import firestore_db

products_blueprint = Blueprint("products", __name__)

PRODUCTS_COLLECTION_NAME = "products"


@products_blueprint.route("/", methods=["GET", "POST"])
def products():
    if flask.request.method == "GET":
        products = firestore_db.collection(PRODUCTS_COLLECTION_NAME).get()
        products_list = [product.to_dict() for product in products]
        return flask.jsonify(products_list)
    else:
        try:
            product_name = flask.request.json["name"]
            product_description = flask.request.json["description"]
            product_price = flask.request.json["price"]
        except KeyError as e:
            return flask.Response(
                status=400, response=f"Missing required key in the body: {e}"
            )
        new_product = {
            "name": product_name,
            "description": product_description,
            "price": product_price,
        }
        _, product_ref = firestore_db.collection(PRODUCTS_COLLECTION_NAME).add(
            new_product
        )
        return flask.jsonify({"id": product_ref.id})


@products_blueprint.route("/<product_id>", methods=["GET", "PUT", "DELETE"])
def product_id(product_id):
    if flask.request.method == "GET":
        product_doc = (
            firestore_db.collection(PRODUCTS_COLLECTION_NAME)
            .document(str(product_id))
            .get()
        )
        if not product_doc.exists:
            return flask.Response(status=404)
        return flask.jsonify(product_doc.to_dict())

    elif flask.request.method == "PUT":
        product_doc = (
            firestore_db.collection(PRODUCTS_COLLECTION_NAME)
            .document(str(product_id))
            .get()
        )
        if not product_doc.exists:
            return flask.Response(status=404)

        for key, value in flask.request.json.items():
            product_doc.reference.update({key: value})
        return flask.Response(status=200)

    elif flask.request.method == "DELETE":
        product_doc = (
            firestore_db.collection(PRODUCTS_COLLECTION_NAME)
            .document(str(product_id))
            .get()
        )
        if not product_doc.exists:
            return flask.Response(status=404)
        product_doc.reference.delete()
        return flask.Response(status=200)
