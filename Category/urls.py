from django.urls import path
from .import views


urlpatterns = [
      path('create_category/', views.create_category, name='create_category'),
]