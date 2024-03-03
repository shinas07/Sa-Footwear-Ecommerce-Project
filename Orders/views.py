from django.shortcuts import render,redirect
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





def order(request):
    return render(request,'order.html')


def check_out(request):
    addresses = Address.objects.filter(user=request.user)
    form = CheckoutForm(user=request.user)
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price for item in cart_items)
    context = {
        'addresses': addresses,
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            address_id = form.cleaned_data['address'].id
            payment_method = form.cleaned_data['payment_method']
            if address_id:
                cart, created = Cart.objects.get_or_create(user=request.user)
                if not created:
                    try:
                        with transaction.atomic():
                            # Calculate total order amount
                            total_amount = cart.calculate_total_amount()

                            # Create payment instance
                            payment = Payment.objects.create(user=request.user, method=payment_method, amount=total_amount)

                            # Create order instance
                            order = Order.objects.create(user=request.user, address_id=address_id, payment=payment, total_amount=total_amount)

                            # Create order items and decrease product quantities
                            for cart_item in CartItem.objects.filter(cart=cart):
                                product = cart_item.product
                                quantity_ordered = cart_item.quantity
                                print(quantity_ordered)
                                
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

                            # Clear cart after successful order placement
                            cart.delete()

                            return redirect('order_confirmation')
                    except Exception as e:
                        return render(request, 'checkout.html', {'addresses': addresses, 'error': str(e), 'form': form})
                else:
                    return render(request, 'checkout.html', {'addresses': addresses, 'error': 'Cart is empty.', 'form': form})
            else:
                return render(request, 'checkout.html', {'addresses': addresses, 'error': 'Please select an address.', 'form': form})
        else:
            print(form.errors)

    return render(request, 'checkout.html', context)





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

    


# def order_distory(request):
#     orders = Order.objects.filter(user=request.user)
#     return render(request,'order_history.html',{'orders':orders})




def order_confimation(request):
    # You can implement this view to display an order confirmation message or details
    return render(request, 'order_complete.html')




















def order_complete(request):
    return render(request,'order_complete.html')