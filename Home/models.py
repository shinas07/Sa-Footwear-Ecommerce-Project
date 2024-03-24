
from django.db import models
from Accounts.models import Customer



class Address(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True,null=True)
    address = models.CharField(max_length=100)
    House_no = models.CharField(max_length=100, blank=True, null=True)
    # address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False,null=True)
    


def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.state}, {self.country}"


class Banner(models.Model):
    banner_name = models.CharField(max_length=50)
    banner_image =models.ImageField()

    def __str__(self):
        return self.banner_name


#Wallet MODEL


class Wallet(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def add_product_price_to_balance(self, amount):
        print(f'amount of wallet is added {amount}')
        self.balance += amount
        self.save()

    def __str__(self):
        return f"Wallet of {self.user.username}"

class CancelOrder(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount_refunded = models.DecimalField(max_digits=10, decimal_places=2)
    # order_product = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)  # Reference to OrderProduct model
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.user.wallet.balance += self.amount_refunded
        self.user.wallet.save()




# class CancelOrderRequest(models.Model):
#     user = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     reason = models.TextField()
#     is_approved = models.BooleanField(default=False)