from django.test import TestCase

from ShoppingAppBackend.models import Item
from ShoppingAppBackend.models import Review


class ItemTestCase(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name='Test Item',
            price=10.99,
            quantity=5,
            details='Test details'
        )

    def test_item_creation(self):
        """Test if item is created correctly"""
        self.assertEqual(self.item.name, 'Test Item')
        self.assertEqual(self.item.price, 10.99)
        self.assertEqual(self.item.quantity, 5)
        self.assertEqual(self.item.details, 'Test details')

    def test_item_update(self):
        """Test updating item fields"""
        self.item.name = 'Updated Item'
        self.item.price = 21
        self.item.quantity = 10
        self.item.details = 'Updated details'
        self.item.save()

        updated_item = Item.objects.get(pk=self.item.pk)
        self.assertEqual(updated_item.name, 'Updated Item')
        self.assertEqual(updated_item.price, 21)
        self.assertEqual(updated_item.quantity, 10)
        self.assertEqual(updated_item.details, 'Updated details')

    def test_item_deletion(self):
        """Test deleting an item"""
        item_id = self.item.id
        self.item.delete()

        with self.assertRaises(Item.DoesNotExist):
            Item.objects.get(pk=item_id)

    def test_item_str_representation(self):
        """Test string representation of the item"""
        self.assertEqual(str(self.item), 'Item object (1)')



class ReviewTestCase(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name='Test Item',
            price=10.99,
            quantity=5,
            details='Test details'
        )
        self.review = Review.objects.create(
            item=self.item,
            user='Test User',
            rating=4,
            comment='Test comment'
        )

    def test_review_creation(self):
        """Test if review is created correctly"""
        self.assertEqual(self.review.item, self.item)
        self.assertEqual(self.review.user, 'Test User')
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, 'Test comment')

    def test_review_item_relationship(self):
        """Test the relationship between review and item"""
        self.assertEqual(self.review.item, self.item)
        self.assertIn(self.review, self.item.review_set.all())

    def test_review_str_representation(self):
        """Test string representation of the review"""
        expected_str = "Review object (1)"
        self.assertEqual(str(self.review), expected_str)

