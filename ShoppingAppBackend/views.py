# views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .Generators.ReviewGenerator import ReviewGenerator
from .Generators.ItemGenerator import ItemGenerator
from .models import Item, Review, CustomUser
from .serializers import ItemSerializer, ReviewSerializer
from django.db.models import Count
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# shopping_cart = ShoppingCart()
# shopping_cart.addItem("apple", 20, 10, "a delicious apple")
# shopping_cart.addItem("pear", 20, 10, "a delicious pear")
# shopping_cart.addItem("refrigerator", 400, 1, "an outstanding refrigerator")
# shopping_cart.addItem("laptop", 800, 5, "a gaming laptop")


if Item.objects.count() < 200:
    ItemGenerator.create_items_with_real_data(100)

if Review.objects.count() < 100:
    ReviewGenerator.generate_reviews_for_items()


@api_view(['GET', 'POST'])
def item_list(request):
    if request.method == 'GET':
        # items = shopping_cart.getAllItems()
        items = Item.objects.all()
        serializer = ItemSerializer.serialize_list(items)
        return Response(serializer, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if (request.data is not None
                and len(request.data) == 4
                and (("name" in request.data)
                     and ("price" in request.data)
                     and ("quantity" in request.data)
                     and ("details" in request.data))):

            item = ItemSerializer.from_representation(request.data)
            if item:
                item.save()
                # shopping_cart.addItem(request.data["name"], request.data["price"], request.data["quantity"],
                #                      request.data["details"])
                return Response(ItemSerializer.to_representation(item),
                                status=status.HTTP_201_CREATED)
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def item_detail(request, pk):
    if Item.objects.filter(pk=pk).exists():
        item = Item.objects.get(pk=pk)
    else:
        return Response("Invalid id", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if 'reviews' in request.GET:  # checks if this is a request for the reviews of the item
            reviews = item.review_set.all()  # Retrieve all reviews for the item
            serializer = ReviewSerializer.serialize_list(reviews)
            return Response(serializer, status=status.HTTP_200_OK)

        return Response(ItemSerializer.to_representation(item),
                        status=status.HTTP_200_OK)  # if it is a simple get, return the found item

    elif request.method == 'PUT':
        if (request.data is not None
                and len(request.data) < 5
                and (("name" in request.data)
                     or ("price" in request.data)
                     or ("quantity" in request.data)
                     or ("details" in request.data))):
            # name = item.get_name()
            # price = item.get_price()
            # quantity = item.get_quantity()
            # details = item.get_details()
            if "name" in request.data:
                item.name = request.data['name']
            if "price" in request.data:
                item.price = request.data['price']
            if "quantity" in request.data:
                item.quantity = request.data['quantity']
            if "details" in request.data:
                item.details = request.data['details']
            item.save()
            return Response(ItemSerializer.to_representation(Item.objects.get(pk=pk)), status=status.HTTP_201_CREATED)
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item.delete()
        return Response(f"Item with id {pk} was successfully deleted", status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'POST':
        if (request.data is not None
                and len(request.data) == 2  # TODO maybe needs to be changed after User is implemented
                and (("rating" in request.data)
                     and ("comment" in request.data))):

            review = ReviewSerializer.from_representation(request.data, item)
            if review:
                review.save()
                return Response(ReviewSerializer.to_representation(review), status=status.HTTP_201_CREATED)

        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def item_filter(request):
    if request.method == 'GET':
        items_with_min_reviews = Item.objects.annotate(review_count=Count('review')).filter(review_count__gte=5)
        serializer = ItemSerializer.serialize_list(items_with_min_reviews)
        return Response(serializer, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == "GET":
        users = CustomUser.objects.all()
        serialized_users = UserSerializer.serialize_list(users)
        return Response(serialized_users, status=status.HTTP_200_OK)

    elif request.method == "POST":
        if (request.data is not None
                and
                (('username' in request.data) and
                 ('password' in request.data) and
                 ('email' in request.data))):
            data = request.data
            user = UserSerializer.from_representation(data)
            user.set_password(data.get('password'))  # Hash the password
            user.email = data.get('email')
            user.save()
            serialized_user = UserSerializer.to_representation(user)
            return Response(serialized_user, status=status.HTTP_201_CREATED)

        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    if request.method == "GET":
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_user = UserSerializer.to_representation(user)
        return Response(serialized_user, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        if 'username' in data:
            user.username = data.get('username', user.username)
        if 'is_manager' in data:
            user.is_manager = data.get('is_manager', user.is_manager)
        if 'is_admin' in data:
            user.is_admin = data.get('is_admin', user.is_admin)
        if 'password' in data:
            user.set_password(data.get('password'))  # Hash the new password
        user.save()

        serialized_user = UserSerializer.to_representation(user)
        return Response(serialized_user, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
    }
    return Response(data, status=status.HTTP_200_OK)