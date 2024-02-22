from django.shortcuts import render
from Products.models import Product,Category
from Category.models import Category
from Home.models import Banner
from django.db.models import Q
# Create your views here.

def home(request):
    active_category = 'home'
    products = Product.objects.filter(Q(category__category_name="Men") | Q(category__category_name='Women'),
        category__is_listed=True,is_available=True)
    lasted_categories = Product.objects.exclude(Q(category__category_name='Men') | Q(category__category_name='Women'))
    banners = Banner.objects.all()
    categorys = Category.objects.all()
    context = {
        'products':products,
        'lasted_categories' :lasted_categories,
        'banners' : banners,
        'categorys':categorys,
        'active_category' : active_category,
    }
    return render(request, 'home.html',context)


# def category_men(request):
#     category = Category.objects.all()
#     return render


