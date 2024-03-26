from django.db import models
from Accounts.models import Customer
from  Home.models import Address
from Products.models import Product

# Create your models here.




class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Razorpay', 'Razorpay'),   
    ]
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)




class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon_id = models.CharField(max_length=100, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_method = models.CharField(max_length=20, choices=[('COD', 'Cash on Delivery'), ('Razorpay', 'Razorpay')], null=True, default=True)
    
    # Address fields with null=True`    `
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    House_no = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Order #{self.name}"




    def cancel_order(self):
        if self.status != 'Cancelled':
            self.status = 'Cancelled'
            self.save()

 

    # payment_method = models.CharField(max_length=10, choices=Payment.PAYMENT_METHOD_CHOICES)



class OrderProduct(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending',null=True)
    review = models.TextField(blank=True, null=True)  # Allow blank and null values for review
    rating = models.IntegerField(default=0, null=True)  # Default rating value can be adjusted as needed
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)  # Reference to the user who submitted the review
    delivery_date = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f" Product: {self.product.product_name} "


