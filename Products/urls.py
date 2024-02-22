from django.urls import path
from . import views

app_name = 'product'


urlpatterns = [
    path('product-details/<int:product_id>/',views.product_detail,name='product_details'),
    path('brand_wise_products/<int:brand_id>/',views.brand_wise_products,name='brand_wise_products'),
    
    path('collections/<str:category_name>/',views.category_collections,name='category_collections'),
]
