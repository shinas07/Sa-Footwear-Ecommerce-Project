from django.shortcuts import render
from Products.models import Product
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def prduct_cart(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(Q(product_brand=product.product_brand) & Q(category=product.category))[:4]
    context = {
        'product':product,
        'related_products' :related_products,
        # 'cart_products': cart_products, 
    }
    return render(request,'cart.html',context)



@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    return JsonResponse({'message': 'Product added to cart successfully!'})
