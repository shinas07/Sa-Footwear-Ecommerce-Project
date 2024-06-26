from datetime import timezone
from decimal import Decimal
from django.shortcuts import render,get_object_or_404,redirect
from Products.models import Product, ProductSizeColor
from django.db.models import Q
from django.http import JsonResponse
from .models import Cart,CartItem
from .forms import AddToCartForm, CoupenApplyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import CustomerCoupon,Coupon
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
# Create your views here.





@login_required(login_url='Accounts:login')
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
            
        product = get_object_or_404(Product, pk=product_id)

        
        size_id = request.POST.get('size_id')
        product_size_color = get_object_or_404(ProductSizeColor, pk=size_id)
        
        if product_size_color.Stock > 0:  # Check if product is in stock
            existing_cart_item = CartItem.objects.filter(cart=cart, product=product)
            if  existing_cart_item:
                messages.warning(request,'Item already in the cart')
                return redirect('view_cart')
            
            form = AddToCartForm(request.POST, product=product)
            if form.is_valid():
                quantity = form.cleaned_data['quantity']
                max_quantity_per_person = 6

                if quantity <= max_quantity_per_person:
                    if quantity <= product_size_color.Stock:
                        # Check if the item already exists in the cart
                        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, product_size_color=product_size_color)
                        if not created:
                            # If the item exists, add the new quantity to the existing quantity
                            total_quantity = cart_item.quantity + quantity
                            if total_quantity <= max_quantity_per_person:
                                cart_item.quantity = total_quantity
                                cart_item.save()
                                messages.success(request, 'Item added to cart successfully.')
                            else:
                                messages.error(request, 'Exceeded maximum quantity per person.')
                        else:
                            # If the item does not exist, create a new cart item
                            cart_item.quantity = quantity
                            cart_item.save()
                            messages.success(request, 'Item added to cart successfully.')

                        return redirect('view_cart')
                    else:
                        messages.error(request, 'Exceeded available stock quantity.')
                else:
                    messages.error(request, 'Exceeded maximum quantity per person.')
            else:
                messages.error(request, 'Please correct the quantity field and try again.')
                return redirect('product:product_details', product_id=product_id)
        else:
            messages.error(request, 'Product is out of stock.')
            return redirect('product:product_details', product_id=product_id)
    
    return redirect('view_cart')




@login_required(login_url='Accounts:login')
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if created:
        cart_items = []
        return render(request, 'cart.html',)
    else:
        cart_items = CartItem.objects.filter(product__is_available=True,product_size_color__is_unlisted=False,cart__user=request.user)


    
    for item in cart_items:
        if item.product.offer_price:
            item.total_price = item.quantity * item.product.offer_price
        else:
            item.total_price = item.quantity * item.product.price

        if item.product_size_color:
            size = item.product_size_color.size

        # else:
        #     item.product_size = "Size not available"



    total_price = sum(item.total_price for item in cart_items)

    coupon_discount = 0.00
    discount_amount = total_price
    if cart.coupon:
        coupon_discount = cart.coupon.discount
        discount_amount = total_price - coupon_discount # Calculate the actual discount amount


    cart.total_amount = discount_amount  # Update the total amount of the cart
    cart.save()


    # Subtract the discount amount from the total price
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'coupon_discount' :coupon_discount,
        'discount_amount' :discount_amount
    }
    return render(request, 'cart.html', context)





@csrf_exempt
@login_required(login_url='/accounts/login/')
def update_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        new_quantity = int(request.POST.get('quantity'))
        if not item_id or not new_quantity:
            return JsonResponse({"status": "error", "message": "Item ID or quantity is missing"}, status=400)

        # Get the current user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return JsonResponse({"status": "error", "message": "User cart not found"}, status=404)

        # Find the CartItem instance for the given product
        try:
            cart_item = CartItem.objects.get(cart=cart, id=item_id)
            product_stock = ProductSizeColor.objects.filter(product=cart_item.product)
      
            if not product_stock.exists():
                return JsonResponse({"status": "error", "message": "Product have no stock"})
            total_stock = sum(stock.Stock for stock in product_stock)
    
            if new_quantity > total_stock:
                return JsonResponse({"status": "error", "message": "Requested quantity exceeds available stock"})
            

            cart_item.quantity = new_quantity
            cart_item.save()

             # Update the stock of the product
            remaining_stock = total_stock - new_quantity
            for p_stock in product_stock:
                p_stock.Stock = remaining_stock
                # product_stock.save()
            
            # cart_items = CartItem.objects.filter(cart__user=request.user)
            # for item in cart_items:
            #     if item.product.offer_price:
            #         item.total_price = item.quantity * item.product.offer_price
            #     else:
            #         item.total_price = item.quantity * item.product.price

            # total_price = sum(item.total_price for item in cart_items)


            cart, created = Cart.objects.get_or_create(user=request.user)
            if created:
                cart_items = [] 
            else:
                cart_items = CartItem.objects.filter(cart__user=request.user)

            
            for item in cart_items:
                if item.product.offer_price:
                    item.total_price = item.quantity * item.product.offer_price
                else:
                    item.total_price = item.quantity * item.product.price




            total_price = sum(item.total_price for item in cart_items)


            coupon_discount = 0.00
            discount_amount = total_price
            if cart.coupon:
                coupon_discount = cart.coupon.discount
                discount_amount = total_price - coupon_discount # Calculate the actual discount amount


            cart.total_amount = discount_amount  # Update the total amount of the cart
            cart.save()

            return JsonResponse({"status": "success", "message": "Cart updated successfully","totalPrice":total_price,"discountAmount":discount_amount})
        except CartItem.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Item not found in cart"})
        except ProductSizeColor.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product stock not found"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


@login_required(login_url='Accounts:login')
def remove_from_cart(request,cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

#coupon
@login_required(login_url='Accounts:login')
def coupon_apply(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        cart, created = Cart.objects.get_or_create(user=request.user)
        user = request.user
        
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code')
            return redirect('view_cart')

        if CustomerCoupon.objects.filter(user=user, coupon=coupon).exists():
            messages.error(request, 'You have already applied this coupon')
            return redirect('view_cart')
        
        if cart.total_amount < coupon.discount:
            messages.error(request, 'Coupon discount cannot exceed the total amount in the cart.')
            return redirect('view_cart')
    

        CustomerCoupon.objects.create(user=user, coupon=coupon)
        
        success, message = cart.apply_coupon(coupon_code)
        
        if success:
            messages.success(request, 'Coupon applied successfully')
        else:
            messages.error(request, message)
        
        return redirect('view_cart')
    else:
        return redirect('view_cart')

@login_required(login_url='Accounts:login')
def remove_coupen(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart,user=request.user)

        if cart.coupon:
            # Get the corresponding CustomerCoupon object
            customer_coupon = CustomerCoupon.objects.filter(user=request.user, coupon=cart.coupon).first()
            if customer_coupon:
                # Delete the CustomerCoupon object from the database
                customer_coupon.delete()

            # Remove the coupon from the cart
            cart.coupon = None
            cart.save()

            messages.success(request, "Coupon removed successfully")
        else:
            messages.info(request, "There is no coupon applied to remove")

        return redirect('view_cart')
    else:
        return redirect('view_cart')
    

