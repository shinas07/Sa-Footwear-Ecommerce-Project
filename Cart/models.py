# from datetime import timezone
from django.db import models
from Accounts.models import Customer
from Products.models import Product
from django.contrib.auth import get_user_model
from django.utils import timezone



class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    

class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    coupon_applied = models.BooleanField(default=False,null=True,blank=True)


    def calculate_total_amount(self):
        total_amount = 0
        cart_items = self.cartitem_set.all()

        for cart_item in cart_items:
            total_amount += cart_item.product.price * cart_item.quantity

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
    quantity = models.PositiveBigIntegerField(default=1)


