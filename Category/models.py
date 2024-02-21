from time import timezone
from django.db import models
from PIL import Image
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_listed = models.BooleanField(default=True)
    image = models.ImageField(upload_to='category_image/',null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)



    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (250,250)
                img.thumbnail(output_size)
                img.save(self.image.path)

    
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = 'category'