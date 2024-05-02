import flask
from flask import Blueprint
from .firestore_db import firestore_db
from .products import PRODUCTS_COLLECTION_NAME

SHOP_COLLECTION_NAME = "shops"

shop_blueprint = Blueprint("shop", __name__)


@shop_blueprint.route("/", methods=["GET", "POST"])
def shop():
    if flask.request.method == "GET":
        shops = firestore_db.collection(SHOP_COLLECTION_NAME).get()
        shops_list = [shop.to_dict() for shop in shops]
        return flask.jsonify(shops_list)

    if flask.request.method == "POST":
        try:
            shop_name = flask.request.json["name"]
            shop_address = flask.request.json["address"]
        except KeyError as e:
            return flask.Response(
                status=400, response=f"Missing required key in the body: {e}"
            )

        new_shop = {
            "name": shop_name,
            "address": shop_address,
        }
        _, shop_ref = firestore_db.collection(SHOP_COLLECTION_NAME).add(new_shop)
        return flask.jsonify({"id": shop_ref.id})

    return flask.Response(status=405)


@shop_blueprint.route("/<shop_id>", methods=["GET", "PUT", "DELETE"])
def shop_id(shop_id):
    if flask.request.method == "GET":
        shop_doc = firestore_db.collection(SHOP_COLLECTION_NAME).document(str(shop_id))
        if not shop_doc.get().exists:
            return flask.Response(status=404)
        return flask.jsonify(shop_doc.get().to_dict())
    if flask.request.method == "PUT":
        shop_doc = firestore_db.collection(SHOP_COLLECTION_NAME).document(str(shop_id))
        if not shop_doc.get().exists:
            return flask.Response(status=404)

        for key, value in flask.request.json.items():
            shop_doc.get().reference.update({key: value})
        return flask.Response(status=200)
    if flask.request.method == "DELETE":
        shop_doc = firestore_db.collection(SHOP_COLLECTION_NAME).document(str(shop_id))
        if not shop_doc.get().exists:
            return flask.Response(status=404)
        shop_doc.get().reference.delete()
        return flask.Response(status=200)

    return flask.Response(status=405)


@shop_blueprint.route("/<shop_id>/products", methods=["GET"])
def shop_products(shop_id):
    if flask.request.method == "GET":
        shop_document = firestore_db.collection(SHOP_COLLECTION_NAME).document(
            str(shop_id)
        )
        if not shop_document.get().exists:
            return flask.Response(
                status=404, response=f"Shop with id {shop_id} not found"
            )

        shop_products = shop_document.collection(PRODUCTS_COLLECTION_NAME).get()
        shop_products_list = [product.to_dict() for product in shop_products]
        return flask.jsonify(shop_products_list)
    else:
        return flask.Response(status=405)


@shop_blueprint.route(
    "/<shop_id>/products/<product_id>", methods=["GET", "POST", "PUT", "DELETE"]
)
def shop_product_id(shop_id, product_id):
    shop_document = firestore_db.collection(SHOP_COLLECTION_NAME).document(str(shop_id))
    if not shop_document.get().exists:
        return flask.Response(status=404, response=f"Shop with id {shop_id} not found")

    if flask.request.method == "GET":
        product_in_shop_doc = shop_document.collection(
            PRODUCTS_COLLECTION_NAME
        ).document(str(product_id))
        if not product_in_shop_doc.get().exists:
            return flask.Response(status=404)
        return flask.jsonify(product_in_shop_doc.get().to_dict())

    if flask.request.method == "POST":
        product_document = firestore_db.collection(PRODUCTS_COLLECTION_NAME).document(
            str(product_id)
        )
        if not product_document.get().exists:
            return flask.Response(
                status=404, response=f"Product with id {product_id} not found"
            )

        product_in_shop_doc = shop_document.collection(
            PRODUCTS_COLLECTION_NAME
        ).document(str(product_id))

        if product_in_shop_doc.get().exists:
            return flask.Response(
                status=400,
                response=f"Product with id {product_id} already exists in shop with id {shop_id}",
            )

        product_data = product_document.get().to_dict()
        product_data.update({"quantity": flask.request.json.get("quantity", 1)})

        firestore_db.collection(SHOP_COLLECTION_NAME).document(str(shop_id)).collection(
            PRODUCTS_COLLECTION_NAME
        ).document(str(product_id)).set(product_data)

        return flask.jsonify({"id": product_id})

    if flask.request.method == "PUT":
        product_in_shop_doc = (
            firestore_db.collection(SHOP_COLLECTION_NAME)
            .document(str(shop_id))
            .collection(PRODUCTS_COLLECTION_NAME)
            .document(str(product_id))
        )

        if not product_in_shop_doc.get().exists:
            return flask.Response(status=404)

        for key, value in flask.request.json.items():
            product_in_shop_doc.get().reference.update({key: value})
        return flask.jsonify({"id": product_id})

    if flask.request.method == "DELETE":
        product_in_shop_doc = shop_document.collection(
            PRODUCTS_COLLECTION_NAME
        ).document(str(product_id))
        if not product_in_shop_doc.get().exists:
            return flask.Response(status=404)

        product_in_shop_doc.get().reference.delete()
        return flask.Response(status=200)

    return flask.Response(status=405)
