from django.urls import path
from .views import user_logout
from .views import Signup,UserLogin,VerifyOTP
from .views import NewPasswordView

app_name = 'Accounts'


urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('password_reset/', VerifyOTP.as_view(), name='password_reset'),  
    path('logout/', user_logout, name='logout'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify_otp'),
    path('new-password/', VerifyOTP.as_view(), name='new_password'),
    path('password-reset/', NewPasswordView.as_view(), name='NewPasswordView'),
]
