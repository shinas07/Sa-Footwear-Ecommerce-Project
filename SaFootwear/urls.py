"""
URL configuration for SaFootwear project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from Admin_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Admin_app.urls')),
    path('',include('Home.urls')),
    path('',include('Accounts.urls')),
    path('',include('Category.urls')),
    path('', include('Products.urls', namespace='product')),
    path('cart/', include('Cart.urls')),
    path('order/',include('Orders.urls')),
    # path('testapi', views.ChartData.as_view()), 
    # path('admin-dashboard/',include('dashboard.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


