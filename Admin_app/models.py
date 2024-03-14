from django.db import models
from Products.models import Product
from django.utils import timezone

# Create your models here.

#Sale Report Model
class Sale(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name
    
#Product Offer Model

class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.end_date < timezone.now().date():
            self.delete()  # Delete the offer if end date has passed
    
    def __str__(self):
        return f"{self.product.product_name} - {self.discount_percentage}% Offer"
    
