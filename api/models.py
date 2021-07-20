from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """
    Product Instance
    """
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    description = models.TextField()
    filename = models.CharField(max_length=128)
    height = models.IntegerField()
    width = models.IntegerField()
    price = models.FloatField()
    rating = models.IntegerField()

    class Meta:
        verbose_name = "product"

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Cart(models.Model):
    """
    Cart Instance
    """
    name = models.CharField(max_length=100, default="Generic Cart")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")
    products = models.ManyToManyField(Product, through='ProductGroup', related_name="products")
    total = models.FloatField(default=0)

    class Meta:
        verbose_name = "cart"

    def __str__(self):
        return self.user.get_short_name() + " - " + self.name

    def __unicode__(self):
        return self.user.get_short_name() + " - " + self.name


class ProductGroup(models.Model):
    """
    ProductGroup Instance
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="product")
    quantity = models.IntegerField(default=1)
