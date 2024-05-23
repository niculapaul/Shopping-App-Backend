import unittest

from ShoppingAppBackend.models import Item
from ShoppingAppBackend.serializers import ItemSerializer


class TestSerializer(unittest.TestCase):
    def test_serializer(self):
        item = Item("Test Item", 5, 5, "Test Details")
        item.set_id(5)
        serializer = ItemSerializer.to_representation(item)
        data = {
            'id': item.get_id(),
            'name': item.get_name(),
            'price': item.get_price(),
            'quantity': item.get_quantity(),
            'details': item.get_details()
        }
        self.assertEqual(serializer, data)

        new_data = {
            'name': item.get_name(),
            'price': item.get_price(),
            'quantity': item.get_quantity(),
            'details': item.get_details()
        }

        new_item = ItemSerializer.from_representation(new_data)
        self.assertEqual(new_item.get_name(), new_data['name'])
        self.assertEqual(new_item.get_price(), new_data['price'])
        self.assertEqual(new_item.get_quantity(), new_data['quantity'])
        self.assertEqual(new_item.get_details(), new_data['details'])
        self.assertEqual(new_item.get_id(), None)


if __name__ == '__main__':
    unittest.main()
