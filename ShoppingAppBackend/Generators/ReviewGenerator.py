from django.utils import timezone
from faker import Faker
import random

from ShoppingAppBackend.models import Item, Review


class ReviewGenerator:

    @staticmethod
    def generate_reviews_for_items():
        fake = Faker()
        items = Item.objects.all()
        for item in items:
            # Generate a random number of reviews for each item
            num_reviews = random.randint(0, 30)
            for _ in range(num_reviews):
                user_name = fake.user_name()  # Generate a random username
                rating = random.randint(1, 5)  # Generate a random rating between 1 and 5
                comment = fake.paragraph()  # Generate a random comment
                Review.objects.create(item=item, user=user_name, rating=rating, comment=comment)
