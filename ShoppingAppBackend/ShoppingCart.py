from ShoppingAppBackend.models import Item


class ShoppingCart:

    def __init__(self):
        self.cartItems = []
        self.next_id = 0

    def addItem(self, name, price, quantity, details):
        item = Item(name, price, quantity, details)
        item.set_id(self.next_id)
        self.cartItems.append(item)
        self.next_id += 1

    def clear(self):
        self.cartItems = []

    def display(self):
        print(self.cartItems)

    def getItem(self, item_id):
        items = [item for item in self.cartItems if item.get_id() == item_id]
        if len(items) == 0:
            return None
        return items[0]

    def getLastAdded(self):
        return self.cartItems[-1]

    def getAllItems(self):
        return self.cartItems

    def updateItem(self, item_id, name, price, quantity, details):
        item = self.getItem(item_id)
        if item is None:
            return "Item not found"
        if name is not None:
            item.set_name(name)

        if price is not None and price > 0:
            item.set_price(price)

        if quantity is not None and quantity > 0:
            item.set_quantity(quantity)

        if details is not None:
            item.set_details(details)

        return "Item updated successfully"

    def deleteItem(self, item_id):
        item = self.getItem(item_id)
        if item is None:
            return "Item not found"

        for i, item in enumerate(self.cartItems):
            if item.get_id() == item_id:
                del self.cartItems[i]
                return "Item deleted successfully"

    def size(self):
        return len(self.cartItems)

