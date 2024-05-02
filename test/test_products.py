import unittest
from src.app import app
from src.products import PRODUCTS_COLLECTION_NAME
from test.common_utilities import delete_all_documents

import random


random_product_name = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
random_product_description = "".join(
    random.choices("abcdefghijklmnopqrstuvwxyz", k=100)
)
random_product_price = random.randint(1, 100)


class TestProductsEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        delete_all_documents(PRODUCTS_COLLECTION_NAME)
        return super().setUp()

    def tearDown(self) -> None:
        delete_all_documents(PRODUCTS_COLLECTION_NAME)
        return super().tearDown()

    def test_get_products_empty(self):
        response = self.app.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_post_products_raises_key_error(self):
        response = self.app.post("/products/", json={})
        self.assertEqual(response.status_code, 400)

    def test_post_products(self):
        response = self.app.post(
            "/products/",
            json={
                "name": random_product_name,
                "description": random_product_description,
                "price": random_product_price,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.product_id = response.json["id"]
        self.assertIn("id", response.json)

        with self.subTest("get product by id"):
            response = self.app.get(f"/products/{self.product_id}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["name"], random_product_name)
            self.assertEqual(response.json["description"], random_product_description)
            self.assertEqual(response.json["price"], random_product_price)


class TestProductsEndpointsWithProductId(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        delete_all_documents(PRODUCTS_COLLECTION_NAME)
        response = self.app.post(
            "/products/",
            json={
                "name": random_product_name,
                "description": random_product_description,
                "price": random_product_price,
            },
        )
        self.product_id = response.json["id"]
        return super().setUp()

    def tearDown(self) -> None:
        delete_all_documents(PRODUCTS_COLLECTION_NAME)
        return super().tearDown()

    def test_get_product_by_id(self):
        # make a subtest for reasserting the product is created
        response = self.app.get(f"/products/{self.product_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], random_product_name)
        self.assertEqual(response.json["description"], random_product_description)
        self.assertEqual(response.json["price"], random_product_price)

    def test_get_product_by_invalid_id(self):
        response = self.app.get("/products/invalid-id")
        self.assertEqual(response.status_code, 404)

    def test_update_product_by_id(self):
        response = self.app.put(
            f"/products/{self.product_id}",
            json={
                "name": random_product_name + "new",
                "description": random_product_description + "new",
                "price": random_product_price + 10,
            },
        )
        self.assertEqual(response.status_code, 200)
        with self.subTest():
            response = self.app.get(f"/products/{self.product_id}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["name"], random_product_name + "new")
            self.assertEqual(
                response.json["description"], random_product_description + "new"
            )
            self.assertEqual(response.json["price"], random_product_price + 10)

    def test_update_product_by_invalid_id(self):
        response = self.app.put("/products/invalid-id", json={})
        self.assertEqual(response.status_code, 404)

    def test_delete_product_by_id(self):
        response = self.app.delete(f"/products/{self.product_id}")
        self.assertEqual(response.status_code, 200)

        with self.subTest():
            response = self.app.get(f"/products/{self.product_id}")
            self.assertEqual(response.status_code, 404)

    def test_delete_product_by_invalid_id(self):
        response = self.app.delete("/products/invalid-id")
        self.assertEqual(response.status_code, 404)
