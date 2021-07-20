from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import Product, Cart, ProductGroup


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductGroupSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    filename = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = ProductGroup
        fields = ['id', 'title', 'description', 'filename', 'price', 'quantity']

    def get_id(self, instance):
        return instance.product.pk

    def get_title(self, instance):
        return instance.product.title

    def get_description(self, instance):
        return instance.product.description

    def get_filename(self, instance):
        return instance.product.filename

    def get_price(self, instance):
        return instance.product.price


class CartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'name', 'products', 'total']

    def get_products(self, instance):
        product_groups = instance.productgroup_set.all()
        return ProductGroupSerializer(product_groups, many=True).data
