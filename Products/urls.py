from django.urls import path
from . import views

app_name = 'product'


urlpatterns = [
    path('product-details/<int:product_id>/',views.product_detail,name='product_details'),
    path('brand_wise_products/<int:brand_id>/',views.brand_wise_products,name='brand_wise_products'),
    
    path('collections/<str:category_name>/',views.category_collections,name='category_collections'),
    path('product/stock/<int:size_id>/', views.stock_of_size, name='stock_of_size'),

    path('product/wishlist',views.wishlist_view,name='wishlist_view'),
    path('product/add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    # path('product/wishlist-to-cart/<int:product_id>/',views.wishlist_to_cart,name='wishlist_to_cart'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

   

]
