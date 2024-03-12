from django.db.models.signals import post_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from Accounts.models import Customer
from Home.models import Wallet 

@receiver(post_save, sender=Customer)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)

@receiver(post_save, sender=Customer)
def save_user_wallet(sender, instance, **kwargs):
    instance.wallet.save()
