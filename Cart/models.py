from django.db import models
from Accounts.models import Customer
from Products.models import Product
from django.contrib.auth import get_user_model
# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')


    def calculate_total_amount(self):
        total_amount = 0
        cart_items = self.cartitem_set.all()

        for cart_item in cart_items:
            total_amount += cart_item.product.price * cart_item.quantity

        return total_amount


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)