# from datetime import timezone
from django.db import models
from Accounts.models import Customer
from Products.models import Product, ProductSizeColor
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date



class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
class CustomerCoupon(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    

class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    coupon_applied = models.BooleanField(default=False,null=True,blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True)


    def calculate_total_amount(self):
        total_amount = 0
        cart_items = self.cartitem_set.all()    

        for cart_item in cart_items:
            product = cart_item.product
            if product.productoffer_set.exists():  # Check if any related ProductOffer exists
                offer = product.productoffer_set.first()  # Assuming there's only one offer per product
                if offer.start_date <= timezone.now().date() <= offer.end_date:
                    total_amount += product.price - (product.price * (offer.discount_percentage / 100)) * cart_item.quantity
                else:
                    total_amount += product.price * cart_item.quantity
            else:
                total_amount += product.price * cart_item.quantity


        return total_amount

    
    def apply_coupon(self, coupon_code):
        try:
            coupon = Coupon.objects.get(code=coupon_code, active=True)
            if coupon.valid_from <= timezone.now().date() <= coupon.valid_to:

                if not self.coupon:
                    self.coupon = coupon
                    self.coupon_applied = True 
                    self.save()
                    return True, "Coupon applied successfully"
                else:
                    return False, "You have already used this coupon"
            else:
                return False, "This coupon is not valid."
        except Coupon.DoesNotExist:
            return False, "Invaild coupon cade." 
    



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product_size_color = models.ForeignKey(ProductSizeColor, on_delete=models.CASCADE, null=True)


