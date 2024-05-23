import unittest

from ShoppingAppBackend.ShoppingCart import ShoppingCart


class TestInMemoryRepository(unittest.TestCase):

    def test_in_memory_repository(self):
        shopping_cart = ShoppingCart()
        shopping_cart.addItem("apple", 20, 10, "a delicious apple")

        self.assertEqual(shopping_cart.getAllItems()[0].get_id(), 0)
        self.assertEqual(shopping_cart.getAllItems()[0].get_name(), "apple")
        self.assertEqual(shopping_cart.getAllItems()[0].get_price(), 20)
        self.assertEqual(shopping_cart.getAllItems()[0].get_quantity(), 10)
        self.assertEqual(shopping_cart.getAllItems()[0].get_details(), "a delicious apple")

        shopping_cart.addItem("pear", 20, 10, "a delicious pear")
        shopping_cart.addItem("refrigerator", 400, 1, "a outstanding refrigerator")
        shopping_cart.addItem("laptop", 800, 5, "a gaming laptop")

        self.assertEqual(shopping_cart.getAllItems()[3].get_id(), 3)
        self.assertEqual(shopping_cart.size(), 4)

        self.assertEqual(shopping_cart.getItem(2).get_name(), "refrigerator")

        self.assertEqual(shopping_cart.getLastAdded().get_name(), "laptop")

        result = shopping_cart.updateItem(10, "apple", 20, 10, "a")
        self.assertEqual(result, "Item not found")

        result = shopping_cart.updateItem(1, "pear_updated", 30, 5, "updated_detail")
        self.assertEqual(result, "Item updated successfully")
        self.assertEqual(shopping_cart.getAllItems()[1].get_id(), 1)
        self.assertEqual(shopping_cart.getAllItems()[1].get_name(), "pear_updated")
        self.assertEqual(shopping_cart.getAllItems()[1].get_price(), 30)
        self.assertEqual(shopping_cart.getAllItems()[1].get_quantity(), 5)
        self.assertEqual(shopping_cart.getAllItems()[1].get_details(), "updated_detail")

        result = shopping_cart.deleteItem(10)
        self.assertEqual(result, "Item not found")

        result = shopping_cart.deleteItem(1)
        self.assertEqual(result, "Item deleted successfully")
        self.assertEqual(shopping_cart.size(), 3)


if __name__ == '__main__':
    unittest.main()
