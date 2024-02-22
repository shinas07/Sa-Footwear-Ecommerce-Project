from django.shortcuts import render, get_object_or_404 
from .models import Product,Brand,Category,ProductSizeColor


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
    brands = Brand.objects.filter(category=category,is_active=True)



    # Set the active category for the template
    active_category = category_name.lower()

    context = {
        'brands': brands,
        'products': products,
        'gender': category_name,
        'category': category,
        'active_category': active_category,

    }
    return render(request,'collection.html',context)



def product_detail(request,product_id):
    product = get_object_or_404(Product, pk=product_id, is_available=True, category__is_listed=True)
    product_size_colors = ProductSizeColor.objects.filter(product_id=product_id)


    return render(request,'product_details.html',{'product':product,'product_size_colors': product_size_colors})

def brand_wise_products(request,brand_id):
    brand = get_object_or_404(Brand,pk=brand_id)
    products = Product.objects.filter(product_brand=brand)
    context = {
        'brand': brand,
        'products': products,
    }
    return render(request, 'collection.html', context)
  