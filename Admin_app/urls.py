from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('admin_users/',views.admin_users,name='admin_users'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock/<int:user_id>/',views.unblock_user,name='unblock_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin_catrgory/',views.admin_category,name='admin_category'),
    path('admin_product/',views.admin_product,name='admin_product'),
    path('admin_add_product/',views.admin_add_product,name='admin_add_product'),
    path('admin_edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('list_product/<int:pk>/', views.list_product, name='list_product'),
    path('unlist_product/<int:pk>/', views.unlist_product, name='unlist_product'),


]
