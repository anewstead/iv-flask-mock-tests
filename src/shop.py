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
    elif flask.request.method == "POST":
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
    else:
        return flask.Response(status=405)


@shop_blueprint.route("/<shop_id>", methods=["GET", "PUT", "DELETE"])
def shop_id(shop_id):
    if flask.request.method == "GET":
        shop_doc = (
            firestore_db.collection(SHOP_COLLECTION_NAME).document(str(shop_id)).get()
        )
        if not shop_doc.exists:
            return flask.Response(status=404)
        return flask.jsonify(shop_doc.to_dict())
    elif flask.request.method == "PUT":
        shop_doc = (
            firestore_db.collection(SHOP_COLLECTION_NAME).document(str(shop_id)).get()
        )
        if not shop_doc.exists:
            return flask.Response(status=404)

        for key, value in flask.request.json.items():
            shop_doc.reference.update({key: value})
        return flask.Response(status=200)
    elif flask.request.method == "DELETE":
        shop_doc = (
            firestore_db.collection(SHOP_COLLECTION_NAME).document(str(shop_id)).get()
        )
        if not shop_doc.exists:
            return flask.Response(status=404)
        shop_doc.reference.delete()
        return flask.Response(status=200)
    else:
        # we should not even get here as we are not allowing other methods but it feels silly to have no else block
        return flask.Response(status=405)


@shop_blueprint.route("/<shop_id>/products", methods=["GET"])
def shop_products(shop_id):
    if flask.request.method == "GET":
        shop_document = (
            firestore_db.collection(SHOP_COLLECTION_NAME).document(str(shop_id)).get()
        )
        if not shop_document.exists:
            return flask.Response(
                status=404, response=f"Shop with id {shop_id} not found"
            )
        shop_products = (
            firestore_db.collection(SHOP_COLLECTION_NAME)
            .document(str(shop_id))
            .collection(PRODUCTS_COLLECTION_NAME)
            .get()
        )
        shop_products_list = [product.to_dict() for product in shop_products]
        return flask.jsonify(shop_products_list)
    else:
        return flask.Response(status=405)


@shop_blueprint.route(
    "/<shop_id>/products/<product_id>",
    methods=["GET", "POST", "PUT", "DELETE"],
)
def shop_product_id(shop_id, product_id):
    if flask.request.method == "GET":
        product_in_shop_doc = (
            firestore_db.collection(SHOP_COLLECTION_NAME)
            .document(str(shop_id))
            .collection(PRODUCTS_COLLECTION_NAME)
            .document(str(product_id))
            .get()
        )
        if not product_in_shop_doc.exists:
            return flask.Response(status=404)
        return flask.jsonify(product_in_shop_doc.to_dict())

    elif flask.request.method == "POST":
        shop_document = (
            firestore_db.collection(SHOP_COLLECTION_NAME).document(str(shop_id)).get()
        )
        if not shop_document.exists:
            return flask.Response(
                status=404, response=f"Shop with id {shop_id} not found"
            )
        product_document = (
            firestore_db.collection(PRODUCTS_COLLECTION_NAME)
            .document(str(product_id))
            .get()
        )
        if not product_document.exists:
            return flask.Response(
                status=404, response=f"Product with id {product_id} not found"
            )
        product_in_shop_doc = (
            firestore_db.collection(SHOP_COLLECTION_NAME)
            .document(str(shop_id))
            .collection(PRODUCTS_COLLECTION_NAME)
            .document(str(product_id))
            .get()
        )

        if product_in_shop_doc.exists:
            return flask.Response(
                status=400,
                response=f"Product with id {product_id} already exists in shop with id {shop_id}",
            )

        product_data = product_document.to_dict()
        product_data.update({"quantity": flask.request.json.get("quantity", 1)})

        firestore_db.collection(SHOP_COLLECTION_NAME).document(str(shop_id)).collection(
            PRODUCTS_COLLECTION_NAME
        ).document(str(product_id)).set(product_data)

        return flask.jsonify({"id": product_id})

    elif flask.request.method == "PUT":
        # stub method for updating a product in a shop by id
        raise NotImplementedError
    elif flask.request.method == "DELETE":
        # stub method for deleting a product in a shop by id
        raise NotImplementedError
    else:
        # we should not even get here as we are not allowing other methods but it feels silly to have no else block
        return flask.Response(status=405)
