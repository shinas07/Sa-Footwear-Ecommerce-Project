from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_listed = models.BooleanField(default=True)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = 'category'