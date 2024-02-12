from django.urls import path
from .import views

app_name = 'category'

urlpatterns = [
       path('category/add/', views.add_category, name='add_category'),  
       path('category/<int:category_id>/list/', views.list_category, name='list_category'),
       path('category/<int:category_id>/unlist',views.unlist_category,name='unlist_category'),
       path('category/<int:category_id>/delete',views.delete_category,name='delete_category'),
       path('category/edit/<int:category_id>', views.edit_category, name='edit_category'),
]