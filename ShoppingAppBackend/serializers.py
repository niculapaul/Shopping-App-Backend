from ShoppingAppBackend.models import Item, Review, CustomUser


class ItemSerializer:
    @staticmethod
    def to_representation(item):
        return {
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'quantity': item.quantity,
            'details': item.details
        }

    @staticmethod
    def serialize_list(items):
        serialized_items = []
        for item in items:
            serialized_items.append(ItemSerializer.to_representation(item))
        return serialized_items

    @staticmethod
    def from_representation(data):
        return Item(
            name=data.get('name'),
            price=data.get('price'),
            quantity=data.get('quantity'),
            details=data.get('details')
        )


class ReviewSerializer:

    @staticmethod
    def to_representation(review):
        return {
            'id': review.id,
            'user': review.user,
            'rating': review.rating,
            'comment': review.comment
        }

    @staticmethod
    def serialize_list(reviews):
        serialized_reviews = []
        for review in reviews:
            serialized_reviews.append(ReviewSerializer.to_representation(review))
        return serialized_reviews

    @staticmethod
    def from_representation(data, item):
        return Review(
            item=item,
            # user=data.get('user'), #TODO uncomment after User is implemented
            rating=data.get('rating'),
            comment=data.get('comment')
        )


class UserSerializer:
    @staticmethod
    def to_representation(user):
        return {
            'id': user.id,
            'username': user.username,
            'is_manager': user.is_manager,
            'is_admin': user.is_admin,
        }

    @staticmethod
    def serialize_list(users):
        serialized_users = []
        for user in users:
            serialized_users.append(UserSerializer.to_representation(user))
        return serialized_users

    @staticmethod
    def from_representation(data):
        return CustomUser(
            username=data.get('username'),
            # password should be hashed when creating user
            is_manager=data.get('is_manager', False),
            is_admin=data.get('is_admin', False),
        )