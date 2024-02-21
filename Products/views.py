from django.shortcuts import render, get_object_or_404 , HttpResponse
from .models import Product,Brand,Category
# Create your views here.


def product(request):
    products = Product.objects.fiter(is_available= True,category__is_listed=True)
    context = {
        'products': products,
    }
    return render(request,'home.html',context)


def category_collections(request,category_name):
    # active_category = category_name
    # Convert the category_name to title case for consistency with the database
    category_name = category_name.title()
    category = get_object_or_404(Category,category_name=category_name)
    products = Product.objects.filter(category__is_listed=True,is_available=True,category=category)
    brands = Brand.objects.filter(category=category)


    # Set the active category for the template
    active_category = category_name.lower()

    context = {
        'brands': brands,
        'products': products,
        'gender': category_name,
        'category': category,
        'active_category': active_category

    }
    return render(request,'collection.html',context)


def men_collections(request):
    active_category = 'men'
    products = Product.objects.filter(category__is_listed=True,is_available=True,category__category_name="Men")
    brands = Brand.objects.filter(category__category_name='Men')
    men_img  = get_object_or_404(Category,category_name='Men')
    context = {
        'brands' : brands,
        'products':products,
        'gender':'Men',
        'category': men_img ,
        'active_category' : active_category
    }
    return render(request,'collection.html',context)

def women_collections(request):
    active_category = 'women'
    products = Product.objects.filter(category__is_listed=True,is_available=True,category__category_name='Women')
    brands = Brand.objects.filter(category__category_name='Women')
    women_img = get_object_or_404(Category,category_name ='Women')
    # try:
    #     women_img  = Category.objects.get(category_name='Men')
    # except Category.DoesNotExist:
    # # Handle the case where the "Men" category does not exist
    #     return HttpResponse("Men category does not exist.")
    context = {
        'brands' : brands,
        'products':products,
        'gender':'Women',
        'category':women_img,
        'active_category': active_category
    }
    return render(request,'collection.html',context)

def product_detail(request,product_id):
    product = get_object_or_404(Product, pk=product_id, is_available=True, category__is_listed=True)
    return render(request,'product_details.html',{'product':product})

def brand_wise_products(request,brand_id):
    brand = get_object_or_404(Brand,pk=brand_id)
    products = Product.objects.filter(product_brand=brand)
    context = {
        'brand': brand,
        'products': products,
    }
    return render(request, 'collection.html', context)
  