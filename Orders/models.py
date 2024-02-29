from django.db import models
from Accounts.models import Customer
from Home.models import Address
from Products.models import Product,ProductSizeColor

# Create your models here.




class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),

    ]
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon_id = models.CharField(max_length=100, blank=True, null=True)
    is_cancelled = models.BooleanField(default=False, null=True)
    payment_method = models.CharField(max_length=10, choices=[('COD', 'Cash on Delivery')], null=True, default=True,)

    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')


    def cancel_order(self):
         self.is_cancelled = True
         self.save()

    # payment_method = models.CharField(max_length=10, choices=Payment.PAYMENT_METHOD_CHOICES)




class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # product_size_color = models.ForeignKey(ProductSizeColor, on_delete=models.CASCADE,null=True,default=True)  # Add this field


def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"

