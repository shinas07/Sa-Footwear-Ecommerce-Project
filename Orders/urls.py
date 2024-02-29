from django.urls import path
from . import views


urlpatterns = [
    path('order/',views.order,name='order'),
    path('checkout/',views.check_out,name='checkout'),
    # path('create_order/',views.create_order,name='create_order'),
    path('order_confimation/', views.order_confimation, name='order_confirmation')

]