from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from products.models import Product, Review, Category
from products.serializers import ProductSerializer, ReviewSerializer, CategorySerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(["GET", "POST"])
def product_list_view(request):
    if request.method == "GET":
        product = Product.objects.all()
        data = ProductSerializer(product, many=True).data
        return Response(data=data)
    elif request.method == "POST":
        title = request.data.get("title")
        description = request.data.get("description")
        cost = request.data.get("cost")
        image = request.data.get("image")
        category_id = request.data.get("category_id")
        product = Product.objects.create(
            title=title,
            description=description,
            cost=cost,
            image=image,
            category_id=category_id,
        )
        return Response(
            data=ProductSerializer(product, status=status.HTTP_201_CREATED).data
        )


@api_view(["GET", "DELETE", "PUT"])
def product_detail_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(
            data={"PRODUCT with this id not found"}, status=status.HTTP_404_NOT_FOUND
        )
    if request.method == "GET":
        data = ProductSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == "DELETE":
        product.delete()
        return Response(ProductSerializer(product), status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        product.title = request.data.get("title")
        product.description = request.data.get("description")
        product.cost = request.data.get("cost")
        product.image = request.data.get("image")
        product.category_id = request.data.get("category_id")
        product.save()
        return Response(
            ProductSerializer(product).data, status=status.HTTP_202_ACCEPTED
        )


@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    User.objects.create_user(username=username, password=password)
    return Response(data={"USER CREATED"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return Response(data={"Key": token.key})
    return Response(data={"USER NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([[IsAuthenticated]])
def user_reviews(request):
    reviews = Review.objects.filter(author=request.data)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(data=serializer.data)


@api_view(["GET"])
def reviews_list(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(reviews, many=True).data
    return Response(data=data)


@api_view(["GET"])
def reviews_detail(request, id):
    reviews = Review.objects.get(id=id)
    data = ReviewSerializer(reviews, many=False).data
    return Response(data=data)


@api_view(["GET"])
def categories(request):
    category = Category.objects.all()
    data = CategorySerializer(category, many=True).data
    return Response(data=data)


@api_view(["GET"])
def categories_id(request, id):
    category = Category.objects.get(id=id)
    data = CategorySerializer(category, many=False).data
    return Response(data=data)
