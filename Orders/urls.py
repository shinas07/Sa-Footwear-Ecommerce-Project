from django.urls import path
from . import views


urlpatterns = [
    path('order/',views.order,name='order'),
    path('checkout/',views.check_out,name='checkout'),
    # path('create_order/',views.create_order,name='create_order'),
    path('order_confimation/', views.order_confimation, name='order_confirmation'),
    path('order_add_address',views.order_add_address,name='order_add_address'),
    path('order_edit_address<int:address_id>',views.order_edit_address,name='order_edit_address')

]