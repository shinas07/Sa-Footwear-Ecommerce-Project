from django.db import models
from Accounts.models import Customer

class Address(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    House_no = models.CharField(max_length=100, blank=True, null=True)
    # address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=20)
    # is_default_shipping = models.BooleanField(default=False,null=True)


def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.state}, {self.country}"



class Banner(models.Model):
    banner_name = models.CharField(max_length=50)
    banner_image =models.ImageField()

    def __str__(self):
        return self.banner_name

