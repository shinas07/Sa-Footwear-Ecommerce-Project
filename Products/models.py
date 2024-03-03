from django.db import models
from Category.models import Category
from PIL import Image
from datetime import datetime

# Create your models here.




class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    brand_image = models.ImageField(upload_to='brand_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True,null=True)



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.brand_image:
            img = Image.open(self.brand_image.path)
            target_size = (300, 300)
            img = img.resize(target_size, Image.BICUBIC)
            img.save(self.brand_image.path)
    
    def __str__(self):
        return self.brand_name




class Product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    product_brand = models.ForeignKey(Brand, on_delete=models.CASCADE,null=True,blank=True) 
    left_view_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    right_view_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    full_view_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now,null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00,null=True)

    def __str__(self):
        return self.product_name
    
class ProductSizeColor(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    Stock = models.IntegerField()
    color = models.CharField(max_length=50,null=True)
    is_unlisted = models.BooleanField(default=False)
    

    def __str__(self):
        return self.product.product_name
class Meta:
    unique_together = ('product','size','color')
    
# class ProductImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'images')
#     image = models.ImageField(upload_to='product_images/')




    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

        #   # Resize left view image
        # if self.left_view_image:
        #     img = Image.open(self.left_view_image.path)
        #     img.thumbnail((300, 300), Image.BICUBIC)
        #     img.save(self.left_view_image.path,quality=100)
        
        # # Resize right view image
        # if self.right_view_image:
        #     img = Image.open(self.right_view_image.path)
        #     img.thumbnail((300, 300), Image.BICUBIC)
        #     img.save(self.right_view_image.path,quality=100)
        
        # # Resize full view image
        # if self.full_view_image:
        #     img = Image.open(self.full_view_image.path)
        #     img.thumbnail((500, 300), Image.BICUBIC)  # Adjust output size as needed
        #     img.save(self.full_view_image.path,quality=100)







