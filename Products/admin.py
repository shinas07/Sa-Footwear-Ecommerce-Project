from django.contrib import admin
from Products.models import Product,ProductSizeColor

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category']
    prepopulated_fields = {'slug': ('product_name',)}  

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSizeColor)