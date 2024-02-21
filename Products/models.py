from django.db import models
from Category.models import Category
from PIL import Image

# Create your models here.
class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

   
    # stock = models.PositiveIntegerField()

class Stock(models.Model):
    product_name = models.CharField(max_length=50)
    product_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product_name
    


    def __str__(self):
        return self.name
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




class ColorVariant(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)  # For storing color code or any other representation

    def __str__(self):
        return self.name
    


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,)
    description = models.CharField(max_length=200)
    size = models.ManyToManyField(Size)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.OneToOneField(Stock,on_delete=models.SET_NULL,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    left_view_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    right_view_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    full_view_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    product_brand = models.ForeignKey(Brand, on_delete=models.CASCADE,null=True,blank=True) 
    color_variant = models.ForeignKey(ColorVariant,on_delete =models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.product_name







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







