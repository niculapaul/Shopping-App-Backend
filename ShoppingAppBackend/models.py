from django.contrib.auth.models import AbstractUser
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    details = models.TextField()

    class Meta:
        db_table = 'Item'


class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.CharField(max_length=100, default="Anonymous User")
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Review'


class CustomUser(AbstractUser):
    # Add custom fields if needed
    is_manager = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = 'CustomUser'
