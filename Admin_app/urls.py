from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('admin_users/',views.admin_users,name='admin_users'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),

    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock/<int:user_id>/',views.unblock_user,name='unblock_user'),
    
    path('admin_catrgory/',views.admin_category,name='admin_category'),

    path('admin_product/',views.admin_product,name='admin_product'),
    path('admin-product-filter/',views.admin_product_filter,name='admin_product_filter'),
    path('admin_add_product/',views.admin_add_product,name='admin_add_product'),
    path('product_size_color/', views.product_size_color, name='product_size_color'),
    path('edit_product_size_color/<int:pk>/',views.edit_product_size_color,name='edit_product_size_color'),

    path('admin_edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('list_product/<int:pk>/', views.list_product, name='list_product'),
    path('unlist_product/<int:pk>/', views.unlist_product, name='unlist_product'),

    path('admin_add_brand', views.admin_add_brand, name='admin_add_brand'),
    path('block_brand/<int:brand_id>',views.block_brand,name='block_brand'),
    path('unblock_brand/<int:brand_id>',views.unblock_brand,name='unblock_brand'),
    path('edit_brand/<int:brand_id>/',views.edit_brand,name='edit_brand'),

    path('admin_order_management/',views.admin_order_management,name='admin_order_management'),

    path('admin-add-banner/', views.admin_add_banner, name='admin_add_banner'),
    path('delete-banner/<int:banner_id>/', views.delete_banner, name='delete_banner'),
    path('admin_products_details/<int:order_id>', views.order_products_details, name='order_products_details'),


    path('admin-add-coupon/', views.admin_add_coupon, name='admin_add_coupon'),
    path('admin-delete-coupon/<int:coupon_id>/',views.admin_delete_coupon, name='admin_delete_coupon'),

    # path('admin_order_details/<int:order_id>/<int:product_id>/', views.admin_order_details, name='admin_order_details'),
    path('admin-product-status/<int:order_id>/<int:order_product_id>/', views.admin_product_status, name='admin_product_status'),

    path('discount-product-list/',views.discount_product_list,name='discount_product_list'),
    path('set-product-discount/<int:product_id>',views.set_product_discount,name='set_product_discount'),

    path('admin-sales-report/',views.admin_sales_report,name='admin_sales_report'),
    path('download-report/', views.download_report, name='download_report'),
    path('best-selling/', views.best_selling, name='best_selling'),

]


