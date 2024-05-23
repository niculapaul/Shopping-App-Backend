# tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from ShoppingAppBackend.ShoppingCart import ShoppingCart


class ShoppingCartTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.shopping_cart = ShoppingCart()
        self.shopping_cart.addItem("apple", 20, 10, "a delicious apple")
        self.shopping_cart.addItem("pear", 20, 10, "a delicious pear")
        self.shopping_cart.addItem("refrigerator", 400, 1, "a outstanding refrigerator")
        self.shopping_cart.addItem("laptop", 800, 5, "a gaming laptop")

    def test_get_item_list(self):
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # Assuming 4 items are added initially

    def test_add_valid_item(self):
        data = {
            "name": "Test Item",
            "price": 9.99,
            "quantity": 10,
            "details": "Test description"
        }
        response = self.client.post('/items/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['price'], data['price'])
        self.assertEqual(response.data['quantity'], data['quantity'])
        self.assertEqual(response.data['details'], data['details'])
        self.assertEqual(response.data['id'], 4)


    def test_add_invalid_item(self):
        data = {}
        response = self.client.post('/items/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_item_detail(self):
        response = self.client.get('/items/2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        data = {
            "name": "Updated Item",
            "price": 19.99,
            "quantity": 20,
            "details": "Updated description"
        }
        response = self.client.put('/items/3/', data, format='json')  # Assuming item ID 3 exists
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['price'], data['price'])
        self.assertEqual(response.data['quantity'], data['quantity'])
        self.assertEqual(response.data['details'], data['details'])
        self.assertEqual(response.data['id'], 3)

        data = {}
        response = self.client.put('/items/3/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_item(self):
        response = self.client.delete('/items/1/')  # Assuming item ID 1 exists
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)