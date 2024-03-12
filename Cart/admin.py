from django.contrib import admin
from .models import Coupon,Cart,CartItem
# Register your models here.

admin.site.register(Cart)
admin.site.register(Coupon)
admin.site.register(CartItem)