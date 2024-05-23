from django.db import transaction
from django.utils import timezone

from faker import Faker

from ShoppingAppBackend.models import Item


class ItemGenerator:

    @staticmethod
    def create_items_with_real_data(count=100):
        fake = Faker()
        items = []
        with transaction.atomic():
            for _ in range(count):
                item = Item(
                    name=fake.word(),
                    price=fake.random_number(digits=2),
                    quantity=fake.random_number(digits=1),
                    details=fake.text()
                )
                items.append(item)
            Item.objects.bulk_create(items)
