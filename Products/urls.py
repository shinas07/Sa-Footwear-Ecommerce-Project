from django.urls import path
from . import views

app_name = 'product'


urlpatterns = [
    path('men-collections/', views.men_collections, name='men_collections'),
    path('women-collections/', views.women_collections, name='women_collections'),
    path('product-details/<int:product_id>/',views.product_detail,name='product_details'),
]
