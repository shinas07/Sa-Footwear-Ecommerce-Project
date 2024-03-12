    
from django.db import models
from django.contrib.auth.models import AbstractUser

import Orders


class Customer(AbstractUser):
    is_blocked = models.BooleanField(default=False) 
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(max_length=50)

    def order_history(self):
        return Orders.objects.filter(user=self)

    
    def __str__(self):
        return self.username
