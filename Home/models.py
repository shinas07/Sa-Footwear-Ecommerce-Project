from django.db import models


class Banner(models.Model):
    banner_name = models.CharField(max_length=50)
    banner_image =models.ImageField()
    def __str__(self):
        return self.banner_name

