from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('user-profile/',views.user_profile,name='user_profile'),
    path('edit-user/',views.edit_user,name='edit_user'),
    path('change-password/',views.change_password,name='change_password'),
    path('otp-verification/',views.otp_verification,name='otp_verification'),
    path('address/',views.address_list,name='address_list'),
    path('address/add/',views.add_address,name='add_address'),
    path('address/<int:address_id>/edit/',views.edit_address,name='edit_address'),
    path('address/<int:address_id>/delete/',views.delete_address,name='delete_address'),
    path('search_results/',views.search_results,name='search_results'),
    path('search_results_price/',views.search_results_price,name='search_results_price'),
    path('order_history/',views.order_history,name='order_history'),

]
