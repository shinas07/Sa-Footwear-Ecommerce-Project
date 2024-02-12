from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('admin_users/',views.user_list,name='admin_users'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock/<int:user_id>/',views.unblock_user,name='unblock_user'),
    # path('catrgory/',views.admin_category,name='admin_category'),
]
