# from django.db import models
# from django.contrib.auth.models import User


# # Create your models here.

# class Customer(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # first_name = models.CharField(max_length=50)
#     # last_name = models.CharField(max_length=50)
#     # phone = models.CharField(max_length=50)
#     # email = models.EmailField(unique=True)
#     # password = models.CharField(max_length=128)
#     is_blocked = models.BooleanField(default=False)
#     is_verified = models.BooleanField(default=False)
#     last_login = models.DateTimeField(null=True, blank=True)


#     def __str__(self):
#         return self.first_name
    
from django.db import models
from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    is_blocked = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(max_length=50)

    # Optionally, you can add any additional fields or methods here
    # def __str__(self):
    #     return self.email
