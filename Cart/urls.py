from django.urls import path
from Cart import views


# app_name = 'Cart'

urlpatterns = [
    path('view-cart/',views.view_cart,name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('coupon-apply',views.coupon_apply, name='coupon_apply'),
    path('remove-coupon',views.remove_coupen,name='remove_coupon'),



]
