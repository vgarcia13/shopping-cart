from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import viewsets

from api.models import Product, Cart, ProductGroup
from api.serializers import ProductSerializer, CartSerializer, UserSerializer


class LogoutViewSet(viewsets.GenericViewSet):
    """
    Logout class instance (destroy sessions variables)
    """
    permission_classes = (IsAuthenticated,)

    queryset = User.objects.first()
    serializer_class = UserSerializer

    def list(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response("logged out", status=200)


class ProductViewSet(APIView):
    """
    Product class instance (retrieve products)
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=200)


class CartViewSet(APIView):
    """
    Cart class instance (retrieve products in cart/add products to cart/update items in cart/remove items from cart)
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        cart = Cart.objects.get(user=user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=200)

    def post(self, request):
        user = request.user
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))

        cart = Cart.objects.get(user=user)

        try:
            product = Product.objects.get(pk=product_id)
            pg = ProductGroup.objects.get_or_create(cart=cart, product=product)
            was_created = pg[1]
            if was_created:
                pg[0].quantity = quantity
            else:
                pg[0].quantity = int(pg[0].quantity + quantity)
            pg[0].save()
            cart_new_total = sum(float(item.product.price * item.quantity) for item in cart.productgroup_set.all())
            cart.total = round(cart_new_total, 2)

            cart.save()
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=200)
        except Product.DoesNotExist:
            return Response("product not found", status=404)

    def put(self, request):
        user = request.user
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))

        cart = Cart.objects.get(user=user)

        try:
            product = Product.objects.get(pk=product_id)
            pg = ProductGroup.objects.get(cart=cart, product=product)
            pg.quantity = int(quantity)
            pg.save()
            cart_new_total = sum(float(item.product.price * item.quantity) for item in cart.productgroup_set.all())
            cart.total = round(cart_new_total, 2)

            cart.save()
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=200)
        except Product.DoesNotExist:
            return Response("product not found", status=404)
        except ProductGroup.DoesNotExist:
            return Response("product not found in cart", status=404)

    def delete(self, request):
        user = request.user
        product_id = int(request.POST.get('product_id'))

        cart = Cart.objects.get(user=user)

        try:
            product = Product.objects.get(pk=product_id)
            pg = ProductGroup.objects.get(cart=cart, product=product)
            pg.delete()
            cart_new_total = sum(float(item.product.price * item.quantity) for item in cart.productgroup_set.all())
            cart.total = round(cart_new_total, 2)

            cart.save()
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=200)
        except Product.DoesNotExist:
            return Response("product not found", status=404)
        except ProductGroup.DoesNotExist:
            return Response("product not found in cart", status=404)


class BuyCartViewSet(APIView):
    """
    BuyCartViewSet class instance (simulates to checkout products in cart)
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        cart = Cart.objects.get(user=user)

        try:
            pg = ProductGroup.objects.filter(cart=cart)
            if pg.count() == 0:
                return Response("your cart is empty. Add some items to continue", status=400)
            total = sum(float(item.product.price * item.quantity) for item in cart.productgroup_set.all())
            message = "Thanks for shopping with us! Your cart total is: ${0}".format(total)
            for item in cart.productgroup_set.all():
                item.delete()
            cart.total = 0
            cart.save()
            data = {'message': message, 'total': total}
            return Response(data, status=200)
        except ProductGroup.DoesNotExist:
            return Response("your cart is empty. Add some items to continue", status=400)



