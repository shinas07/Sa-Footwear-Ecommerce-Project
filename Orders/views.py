from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from .models import Address
from Accounts.models import Customer
from Products.models import Product, ProductSizeColor
from .forms import CheckoutForm
from Cart.models import Cart, CartItem  
from django.shortcuts import render, redirect
from .models import Order, OrderProduct, Payment 
from .forms import CheckoutForm
from django.db import transaction
from django.db.models import F
from django.contrib import messages
from Home.forms import AddressForm
from django.contrib.auth.decorators import login_required




@login_required(login_url='Accounts:login')
def order(request):
    return render(request,'order.html')



#COD
@login_required(login_url='Accounts:login')
def check_out(request):
    addresses = Address.objects.filter(user=request.user)
    form = CheckoutForm(user=request.user)
    cart,create = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.all()
    if not cart.cartitem_set.exists():  # Check if the cart has any associated cart items
        messages.error(request, 'There are no products in your cart.')
        return redirect('view_cart')
    

    total_price = 0
    for item in cart_items:
        if item.product.offer_price:
             item.total_price = item.quantity * item.product.offer_price
        else:
            item.total_price = item.quantity * item.product.price
        total_price += item.total_price

    coupon_discount = 0.00
    discount_amount = total_price
    if cart.coupon:
        coupon_discount = cart.coupon.discount
        discount_amount = total_price - coupon_discount

    cart_item_details = []
    for item in cart_items:
        cart_item_details.append({
            'product_name': item.product.product_name,
            'quantity': item.quantity,
            'total_price': item.total_price,
        })


    context = {
        'addresses': addresses,
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
        'coupon_discount': coupon_discount,
        'discount_amount': discount_amount,
        'cart_item_details': cart_item_details,
        'user_info': {
            'name': request.user.username,
            'email': request.user.email,
            'contact': request.user.phone,
        }
    }

    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            address_id = form.cleaned_data['address'].id
            payment_method = form.cleaned_data['payment_method']
            # coupon_id = form.cleaned_data['coupon_id']

            if address_id:
                cart, created = Cart.objects.get_or_create(user=request.user)
                if not created:
                    try:
                        with transaction.atomic():
                            # Calculate total order amount
                            total_amount = cart.calculate_total_amount()

                            # Create payment instance
                            coupon_discount = 0.00
                            if cart.coupon:
                                coupon_discount = cart.coupon.discount
                                total_amount = total_price - coupon_discount

                            payment = Payment.objects.create(user=request.user, method=payment_method, amount=total_amount)

                            # Create order instance
                            order = Order.objects.create(user=request.user, address_id=address_id, payment=payment, total_amount=total_amount,payment_method=payment_method, coupon_id=cart.coupon.discount)
                         

                            # Create order items and decrease product quantities
                            for cart_item in CartItem.objects.filter(cart=cart):
                                product = cart_item.product
                                quantity_ordered = cart_item.quantity
              
                                
                                # Retrieve ProductSizeColor instance
                                product_size_colors = ProductSizeColor.objects.filter(product=product)
                                if product_size_colors.exists():
                                    product_size_color = product_size_colors.first()
                                    if product_size_color.Stock < quantity_ordered:
                                        messages.error(request, f"Sorry, '{product.product_name}' is out of stock.")
                                        return redirect('Cart:view_cart')
                                    # Assuming you want to decrease the stock of the first ProductSizeColor instance
                                    product_size_color.Stock = F('Stock') - quantity_ordered

                                    product_size_color.save()

                                    # Create order item
                                    OrderProduct.objects.create(order=order, product=product, quantity=quantity_ordered)

                            cart.delete()
                            return redirect('order_complete')

                        
                    except Exception as e:
                        return render(request, 'checkout.html', {'addresses': addresses, 'error': str(e), 'form': form})
                else:
           
                    return render(request, 'checkout.html', {'addresses': addresses, 'error': 'Cart is empty.', 'form': form})
              
            else:

                return render(request, 'checkout.html', {'addresses': addresses, 'error': 'Please select an address.', 'form': form})
        else:

            messages.error(request, "Form is not valid. Please check your input.")
            return render(request, 'checkout.html',  {'addresses': addresses, 'error': 'Please select an address.', 'form': form})
        
    return render(request, 'checkout.html', context)




@login_required(login_url='Accounts:login')
def order_add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)    
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "New Address added Success")
            return redirect('checkout')
    else:
        form = AddressForm()
    return render(request, 'order_add_address.html', {'form': form})

def order_edit_address(request,address_id):
    address = Address.objects.get(pk=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST,instance=address)
        if form.is_valid():
            form.save()
            return redirect('checkout')
    else:
        form = AddressForm(instance=address)
    return render(request, 'order_edit_address.html',{'form':form})


# @login_required(login_url='Accounts:login')
# def razorpaycheck(request):
#     cart_items = CartItem.objects.filter(cart__user=request.user)
#     total_price = sum(item.product.price * item.quantity for item in cart_items)
#     cart = Cart.objects.get(user=request.user)
#     coupon_discount = 0.00
#     if cart.coupon:
#         coupon_discount = cart.coupon.discount
#         total_price -= coupon_discount

#     for item in cart_items:
#         if item.product.offer_price:
#             item.total_price = item.quantity * item.product.offer_price
#             print('haai')
#         else:
#             item.total_price = item.quantity * item.product.price
#         total_price += item.total_price    

#     return JsonResponse({
#         'total_price':total_price,
#     })


from django.http import JsonResponse

@login_required(login_url='Accounts:login')
def razorpaycheck(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = 0
    for item in cart_items:
        if item.product.offer_price:
            item.total_price = item.quantity * item.product.offer_price
        else:
            item.total_price = item.quantity * item.product.price
        total_price += item.total_price

    cart = Cart.objects.get(user=request.user)
    coupon_discount = 0.00
    if cart.coupon:
        coupon_discount = cart.coupon.discount
        total_price -= coupon_discount

    return JsonResponse({
        'total_price': total_price,
    })



# razorpay
@login_required(login_url='Accounts:login')
def place_order(request):
    if request.method == 'POST':
        selected_address = request.POST.get('selectedAddress')
        payment_mode = request.POST.get('payment_mode')
        payment_id = request.POST.get('payment_id')
        # coupon_id = request.POST.get('coupon_id')
        cart = Cart.objects.get(user=request.user)

        cart_items = CartItem.objects.filter(cart__user=request.user)

        total_price = 0 
        for item in cart_items:
            if item.product.offer_price:
                item.total_price = item.quantity * item.product.offer_price
            else:
                item.total_price = item.quantity * item.product.price
            total_price += item.total_price
 

        total_amount = total_price
        coupon_discount = 0.00
        if cart.coupon:
            coupon_discount = cart.coupon.discount
            total_amount -= coupon_discount
        
        # Create the payment instance
        payment = Payment.objects.create(
            user=request.user, 
            method=payment_mode, 
            amount=total_amount
        )
        # Create the order instance
        order = Order.objects.create(
            user=request.user, 
            address_id=selected_address, 
            payment=payment,
            total_amount=total_amount,
            payment_method=payment_mode,
            coupon_id=cart.coupon.discount if cart.coupon else None  # Save the coupon ID with the order if exists# Save the coupon ID with the order
        ) 

        # Retrieve the user's cart
        cart = Cart.objects.get(user=request.user)

        # Loop through cart items
        for cart_item in CartItem.objects.filter(cart=cart):
            product = cart_item.product
            quantity_ordered = cart_item.quantity

            # Retrieve product size color
            product_size_colors = ProductSizeColor.objects.filter(product=product)
            if product_size_colors.exists():
                product_size_color = product_size_colors.first()
                if product_size_color.Stock < quantity_ordered:
                    messages.error(request, f"Sorry, '{product.product_name}' is out of stock.")
                    return redirect('Cart:view_cart')
                # Update product stock
                product_size_color.Stock = F('Stock') - quantity_ordered
                product_size_color.save()
                OrderProduct.objects.create(order=order, product=product, quantity=quantity_ordered)

        cart.delete()

        # Optionally, you can return a success response
        return JsonResponse({'status': 'success'})

    else:
        # If the request method is not POST, return an error response
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'canceld':
        messages.error(request, 'Order is already canceld')
        return redirect('order_detail')


@login_required(login_url='Accounts:login')
def order_complete(request):
    return render(request, 'order_complete.html')















# def order_complete(request):
#     return render(request,'order_complete.html')