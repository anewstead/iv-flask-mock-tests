import unittest
from src.app import app
from test.common_utilities import delete_all_documents

import random

random_shop_name = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
random_shop_address = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=100))
random_product_name = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
random_product_description = "".join(
    random.choices("abcdefghijklmnopqrstuvwxyz", k=100)
)
random_product_price = random.randint(1, 100)


class TestShopEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        delete_all_documents()
        return super().setUp()

    def tearDown(self) -> None:
        delete_all_documents()
        return super().tearDown()

    def test_post_shop_raises_key_error(self):
        response = self.app.post("/shop/", json={})
        self.assertEqual(response.status_code, 400)

    def test_post_shop(self):
        response = self.app.post(
            "/shop/",
            json={
                "name": random_shop_name,
                "address": random_shop_address,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.shop_id = response.json["id"]
        self.assertIn("id", response.json)

        with self.subTest("get shop by id"):
            response = self.app.get(f"/shop/{self.shop_id}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["name"], random_shop_name)
            self.assertEqual(response.json["address"], random_shop_address)


class TestShopEndpointsWithShopId(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        delete_all_documents()
        response = self.app.post(
            "/shop/",
            json={
                "name": random_shop_name,
                "address": random_shop_address,
            },
        )
        self.shop_id = response.json["id"]
        return super().setUp()

    def tearDown(self) -> None:
        delete_all_documents()
        return super().tearDown()

    def test_get_shop_by_id(self):
        response = self.app.get(f"/shop/{self.shop_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], random_shop_name)
        self.assertEqual(response.json["address"], random_shop_address)

    def test_get_shop_by_invalid_id(self):
        response = self.app.get(f"/shop/invalid_id")
        self.assertEqual(response.status_code, 404)

    def test_update_shop_by_id(self):
        new_shop_name = random_shop_name + "new"
        new_shop_address = random_shop_address + "new"
        response = self.app.put(
            f"/shop/{self.shop_id}",
            json={
                "name": new_shop_name,
                "address": new_shop_address,
            },
        )

        self.assertEqual(response.status_code, 200)
        with self.subTest("get shop by id"):
            response = self.app.get(f"/shop/{self.shop_id}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["name"], new_shop_name)
            self.assertEqual(response.json["address"], new_shop_address)

    def test_delete_shop_by_id(self):
        response = self.app.delete(f"/shop/{self.shop_id}")
        self.assertEqual(response.status_code, 200)

        with self.subTest():
            response = self.app.get(f"/shop/{self.shop_id}")
            self.assertEqual(response.status_code, 404)

    def test_delete_shop_by_invalid_id(self):
        response = self.app.delete(f"/shop/invalid_id")
        self.assertEqual(response.status_code, 404)


class TestShopEndpointAddingProducts(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        delete_all_documents()
        product_response = self.app.post(
            "/products/",
            json={
                "name": random_product_name,
                "description": random_product_description,
                "price": random_product_price,
            },
        )
        self.product_id = product_response.json["id"]
        shop_response = self.app.post(
            "/shop/",
            json={
                "name": random_shop_name,
                "address": random_shop_address,
            },
        )
        self.shop_id = shop_response.json["id"]
        return super().setUp()

    def tearDown(self) -> None:
        delete_all_documents()
        return super().tearDown()

    def test_get_shop_products(self):
        response = self.app.get(f"/shop/{self.shop_id}/products")
        self.assertEqual(response.status_code, 200)

    def test_get_shop_products_invalid_id(self):
        response = self.app.get(f"/shop/invalid_id/products")
        self.assertEqual(response.status_code, 404)

    def test_get_shop_products_by_specific_product_id_invalid_id(self):
        response = self.app.get(f"/shop/{self.shop_id}/products/invalid_id")
        self.assertEqual(response.status_code, 404)

    def test_post_shop_products(self):
        quantity = random.randint(1, 100)
        response = self.app.post(
            f"/shop/{self.shop_id}/products/{self.product_id}",
            json={"quantity": quantity},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", response.json)
        product_id = response.json["id"]

        with self.subTest():
            response = self.app.get(f"/shop/{self.shop_id}/products/{product_id}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["name"], random_product_name)
            self.assertEqual(response.json["description"], random_product_description)
            self.assertEqual(response.json["price"], random_product_price)
            self.assertEqual(response.json["quantity"], quantity)

    def test_post_shop_products_invalid_shop_id(self):
        response = self.app.post(
            f"/shop/invalid_id/products/{self.product_id}",
            json={},
        )
        self.assertEqual(response.status_code, 404)

    def test_post_shop_products_invalid_product_id(self):
        response = self.app.post(
            f"/shop/{self.shop_id}/products/invalid_id",
            json={},
        )
        self.assertEqual(response.status_code, 404)

    def test_post_shop_products_invalid_shop_id_and_product_id(self):
        response = self.app.post(
            f"/shop/invalid_id/products/invalid_id",
            json={},
        )
        self.assertEqual(response.status_code, 404)


class TestShopEndpointGettingProductsInShopWithPriceFilters(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        delete_all_documents()
        shop_response = self.app.post(
            "/shop/",
            json={
                "name": random_shop_name,
                "address": random_shop_address,
            },
        )
        self.shop_id = shop_response.json["id"]
        product_1 = self.app.post(
            "/products/",
            json={
                "name": "10",
                "description": "10 quid product",
                "price": 10,
            },
        )

        product_2 = self.app.post(
            "/products/",
            json={
                "name": "20",
                "description": "20 quid product",
                "price": 20,
            },
        )

        product_3 = self.app.post(
            "/products/",
            json={
                "name": "25",
                "description": "25 quid product",
                "price": 25,
            },
        )

        product_4 = self.app.post(
            "/products/",
            json={
                "name": "30",
                "description": "30 quid product",
                "price": 30,
            },
        )

        self.app.post(
            f"/shop/{self.shop_id}/products/{product_1.json['id']}",
            json={"quantity": 1},
        )

        self.app.post(
            f"/shop/{self.shop_id}/products/{product_2.json['id']}",
            json={"quantity": 1},
        )

        self.app.post(
            f"/shop/{self.shop_id}/products/{product_3.json['id']}",
            json={"quantity": 1},
        )

        self.app.post(
            f"/shop/{self.shop_id}/products/{product_4.json['id']}",
            json={"quantity": 1},
        )

        return super().setUp()

    def tearDown(self) -> None:
        delete_all_documents()
        return super().tearDown()

    def test_get_shop_products_with_min_price_filter(self):
        response = self.app.get(f"/shop/{self.shop_id}/products/?min_price=20")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(response.json[0]["price"], 20)
        self.assertEqual(response.json[1]["price"], 25)
        self.assertEqual(response.json[2]["price"], 30)

    def test_get_shop_products_with_max_price_filter(self):
        response = self.app.get(f"/shop/{self.shop_id}/products/?max_price=20")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]["price"], 10)
        self.assertEqual(response.json[1]["price"], 20)

    def test_get_shop_products_with_min_and_max_price_filter(self):
        response = self.app.get(
            f"/shop/{self.shop_id}/products/?min_price=20&max_price=25"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]["price"], 20)
        self.assertEqual(response.json[1]["price"], 25)


class TestShopEndpointEditingProductsInShop(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        delete_all_documents()
        product_response = self.app.post(
            "/products/",
            json={
                "name": random_product_name,
                "description": random_product_description,
                "price": random_product_price,
            },
        )
        self.product_id = product_response.json["id"]
        shop_response = self.app.post(
            "/shop/",
            json={
                "name": random_shop_name,
                "address": random_shop_address,
            },
        )
        self.shop_id = shop_response.json["id"]
        adding_product_to_shop_response = self.app.post(
            f"/shop/{self.shop_id}/products/{self.product_id}",
            json={"quantity": 1},
        )
        self.product_in_shop_id = adding_product_to_shop_response.json["id"]
        return super().setUp()

    def tearDown(self) -> None:
        delete_all_documents()
        return super().tearDown()

    def test_post_shop_products_product_already_exists(self):
        response = self.app.post(
            f"/shop/{self.shop_id}/products/{self.product_id}",
            json={},
        )
        self.assertEqual(response.status_code, 400)

    def test_update_shop_products_details(self):
        quantity = random.randint(2, 100)
        response = self.app.put(
            f"/shop/{self.shop_id}/products/{self.product_id}",
            json={"quantity": quantity},
        )
        self.assertEqual(response.status_code, 200)
        product_id = response.json["id"]

        with self.subTest():
            response = self.app.get(f"/shop/{self.shop_id}/products/{product_id}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["quantity"], quantity)

    def test_update_shop_products_details_invalid_shop_id(self):
        response = self.app.put(
            f"/shop/invalid_id/products/{self.product_id}",
            json={},
        )
        self.assertEqual(response.status_code, 404)

    def test_update_shop_products_details_invalid_product_id(self):
        response = self.app.put(
            f"/shop/{self.shop_id}/products/invalid_id",
            json={},
        )
        self.assertEqual(response.status_code, 404)

    def test_update_shop_products_details_invalid_shop_id_and_product_id(self):
        response = self.app.put(
            f"/shop/invalid_id/products/invalid_id",
            json={},
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_shop_products_invalid_shop_id(self):
        response = self.app.delete(
            f"/shop/invalid_id/products/{self.product_id}",
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_shop_products_invalid_product_id(self):
        response = self.app.delete(
            f"/shop/{self.shop_id}/products/invalid_id",
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_shop_products(self):
        response = self.app.delete(
            f"/shop/{self.shop_id}/products/{self.product_id}",
        )
        self.assertEqual(response.status_code, 200)

        with self.subTest():
            response = self.app.get(f"/shop/{self.shop_id}/products/{self.product_id}")
            self.assertEqual(response.status_code, 404)
