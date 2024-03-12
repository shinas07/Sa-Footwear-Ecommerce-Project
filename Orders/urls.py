from django.urls import path
from . import views


urlpatterns = [
    path('order/',views.order,name='order'),
    path('checkout', views.check_out, name='checkout'),
    # path('create_order/',views.create_order,name='create_order'),
    path('order_add_address',views.order_add_address,name='order_add_address'),
    path('order_edit_address<int:address_id>',views.order_edit_address,name='order_edit_address'),
    path('proceed-to-pay',views.razorpaycheck, name='proceed-to-pay'),
    path('place-order', views.place_order, name='place_order'),
    path('order_complete', views.order_complete, name='order_complete'),
# 
]