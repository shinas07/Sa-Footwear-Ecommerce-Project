from django.shortcuts import render,redirect
from .models import Address
from Accounts.models import Customer
from Products.models import Product
from .forms import CheckoutForm
from Cart.models import Cart, CartItem  
from django.shortcuts import render, redirect
from .models import Order, OrderProduct, Payment 
from .forms import CheckoutForm



def order(request):
    return render(request,'order.html')





def check_out(request):
    addresses = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            address_id = form.cleaned_data['address'].id
            payment_method = form.cleaned_data['payment_method']
            if address_id:
                cart, created = Cart.objects.get_or_create(user=request.user)
                if not created:
                    try:
                        payment = Payment.objects.create(user=request.user, method=payment_method, amount=0)
                        order = Order.objects.create(user=request.user, address_id=address_id, payment=payment)
                        for cart_item in CartItem.objects.filter(cart=cart):
                            OrderProduct.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
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
    else:
        form = CheckoutForm(user=request.user)
    return render(request, 'checkout.html', {'addresses': addresses, 'form': form})

# def create_order(request):
#     user = request.user
#     customer = Customer.objects.get(username=user)
#     address = Address.objects.get(user=customer)


#     payment = Payment.objects.create(user=customer, method='COD',amount=400)  # You need to define calculate_order_total() function
#     order = Order.objects.create(user=customer, address=address, payment=payment)
#     # print(ord)

#     for product_id, quantity in request.POST.items():
#         if product_id.isdigit():
#             product = Product.objects.get(id=product_id)
#             OrderProduct.objects.create(order=order, product=product, quantity=quantity)
#     return redirect('order_confirmation')



# def create_order(request):
#     if request.method == 'POST':
#         order_form = OrderForm(request.POST)
#         if order_form.is_valid():
#             order = order_form.save(commit=False)
#             order.user = request.user
#             order.save()

#             for product_id, quantity in request.POST.items():
#                 if product_id.startswith('product_') and quantity.isdigit():
#                     product = Product.objects.get(id=product_id.split('_')[1])
#                     OrderProduct.objects.create(order=order, product=product, quantity=quantity)

#             return redirect('order_confirmation')
#     else:
#         order_form = OrderForm()
#         order_product_form = OrderProductForm()

#     return render(request, 'create_order.html', {'order_form': order_form, 'order_product_form': order_product_form})






def order_confimation(request):
    # You can implement this view to display an order confirmation message or details
    return render(request, 'order_complete.html')




















def order_complete(request):
    return render(request,'order_complete.html')