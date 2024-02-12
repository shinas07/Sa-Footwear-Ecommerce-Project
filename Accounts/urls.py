from django.urls import path
# from accounts import views
from .views import Signup,UserLogin

app_name = 'Accounts'

urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/',UserLogin.as_view(),name='login'),
]