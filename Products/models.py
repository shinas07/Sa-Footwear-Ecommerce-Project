from django.db import models
from Category.models import Category

# Create your models here.
class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,)
    description = models.CharField(max_length=200)
    size = models.ManyToManyField(Size)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    left_view_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    right_view_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    full_view_image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.product_name

# class ProductImage(models.Model):
#     product = models.ForeignKey(Product,related_name='images',on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='product_images/')
#     view = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.product} - {self.view}"

