from django.urls import path
from Cart import views


app_name = 'Cart'

urlpatterns = [
    path('product-cart/<int:product_id>/',views.prduct_cart,name='product_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
