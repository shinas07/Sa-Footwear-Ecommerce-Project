from django.shortcuts import render,get_object_or_404,redirect
from Products.models import Product
from django.db.models import Q
from django.http import JsonResponse
from .models import Cart,CartItem
from .forms import AddToCartForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


# @login_required
# def prduct_cart(request):
#     related_products = Product.objects.filter(Q(product_brand=product.product_brand) & Q(category=product.category))[:4]
#     context = {

#         'related_products' :related_products,
#         # 'cart_products': cart_products, 
#     }
#     return render(request,'cart.html',context)

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
            
        product = get_object_or_404(Product, pk=product_id)
        product_size_color = product.productsizecolor_set.first()
        
        if product_size_color.Stock > 0:  # Check if product is in stock
            form = AddToCartForm(request.POST, product=product)
            if form.is_valid():
                quantity = form.cleaned_data['quantity']
                max_quantity_per_person = 5

                if quantity < max_quantity_per_person:
                    if quantity <= product_size_color.Stock:
                        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                        if not created:
                            cart_item.quantity += quantity  
                            cart_item.save()
                        else:
                            cart_item.quantity = quantity  
                            cart_item.save()
                        messages.success(request, 'Item added to cart successfully.')
                        return redirect('Cart:view_cart')
                    else:
                        messages.error(request, 'Exceeded maximum quantity per person.')
                        return redirect('product:product_details', product_id=product_id)
                else:
                    messages.error(request,'"Maximum quantity allowed per person exceeded. Please adjust the quantity and try again.')
                    return redirect('product:product_details', product_id=product_id)
            else:
                messages.error(request, 'Please correct the quantity field and try again.')
                return redirect('product:product_details', product_id=product_id)
        else:
            messages.error(request, 'Product is out of stock.')
            return redirect('product:product_details', product_id=product_id)
    
    return redirect('Cart:view_cart')






@login_required
def view_cart(request):
    # Retrieve the cart for the current user, if it exists
    cart, created = Cart.objects.get_or_create(user=request.user)
    if created:
        cart_items = [] 
    else:
        # Retrieve cart items associated with the cart
        cart_items = CartItem.objects.all()
    
    total_price = sum(item.product.price for item in cart_items)
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)




@login_required
def remove_from_cart(request,cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('Cart:view_cart')

