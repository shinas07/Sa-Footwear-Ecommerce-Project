from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('home-filter/',views.home_filter,name='home_filter'),
    
    path('user-profile/',views.user_profile,name='user_profile'),
    path('edit-user/',views.edit_user,name='edit_user'),
    path('change-password/',views.change_password,name='change_password'),
    path('otp-verification/',views.otp_verification,name='otp_verification'),
    path('address/',views.address_list,name='address_list'),
    path('address/add/',views.add_address,name='add_address'),
    path('address/<int:address_id>/edit/',views.edit_address,name='edit_address'),
    path('address/<int:address_id>/delete/',views.delete_address,name='delete_address'),
    path('search_results/',views.search_results,name='search_results'),
    path('search_filter_result/',views.search_filter_result,name='search_filter_result'),

    path('order_history/',views.order_history,name='order_history'),
    path('order_details/<int:order_id>/', views.order_details, name='order_details'),

    path('cancel_product/<int:order_product_id>',views.cancel_product,name='cancel_product'),
    path('product_return/<int:order_product_id>',views.product_return,name='product_return'),
    path('submit_review_and_rating/', views.submit_review_and_rating, name='submit_review_and_rating'),

    path('user/wallet/',views.wallet_balance,name='wallet'),
    path('about/',views.about_page,name='about')
  
]