from django.contrib import admin
from Home.models import Banner,Address,Wallet,CancelOrder

# Register your models here.

admin.site.register(Address)
admin.site.register(Banner) 
admin.site.register(Wallet)
admin.site.register(CancelOrder)