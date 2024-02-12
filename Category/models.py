from django.db import models

# Create your models here.

class Category(models.Model):
    Category_name = models.CharField(max_length=100)
    decription = models.TextField(blank=True)
    
    def __str__(self):
        return self.name