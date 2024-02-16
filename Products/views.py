from django.shortcuts import render, get_object_or_404
from .models import Product,Category
# Create your views here.


def product(request):
    products = Product.objects.all().fiter(is_available= True)
    context = {
        'products': products,
    }
    return render(request,'home.html',context)


def men_collections(request):
    products = Product.objects.all()
    return render(request,'men.html',{'products':products})




def women_collections(request):
    women_category = Category.objects.get(category_name='woman')
    products = Product.objects.filter(category=women_category)
    return render(request,'women.html',{'products':products})

def product_detail(request,product_id):
    product = get_object_or_404(Product,pk=product_id)
    return render(request,'product_details.html',{'product':product})