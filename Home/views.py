from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from Home.forms import ChangePasswordForm,AddressForm
from .models import Customer
from django.contrib.auth.forms import PasswordChangeForm
from Products.models import Product,Category
from Category.models import Category
from Home.models import Banner,Address
from django.db.models import Q
from django.core.mail import send_mail
from allauth.socialaccount.models import SocialApp
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.core.validators import RegexValidator
import random
import string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from Accounts.models import Customer
from django.utils import timezone
from datetime import datetime,timedelta
from Orders.models import OrderProduct,Order

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

    
def user_profile(request):
    user = request.user
    return render(request,'user_profile.html',{'user':user})





def edit_user(request):
    user = request.user
    if request.method == 'POST':
        user_model = get_user_model()
        user = user_model.objects.get(pk=request.user.pk)
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        new_email = request.POST.get('email')
        old_email = user.email
        user.phone = request.POST.get('phone')

        error_message = validate_user_data(request.POST)
        if error_message:
            return render(request, 'edit_profile.html', {'error': error_message, 'user': user})

        if new_email != old_email:
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['new_email'] = new_email 

            user_data = {
                'username': request.POST.get('username'),
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone')
            }

            request.session['user_data'] = user_data


            send_otp_email(new_email,otp)
            otp_verification(request)
            return redirect('otp_verification')
        else:
            user.save()
            messages.success(request, 'User details updated successfully!')
            return redirect('user_profile')
    return render(request, 'edit_profile.html', {'user': user})


def validate_user_data(post_data):
    error_message = None
    
    email_validator = EmailValidator()
    try:
        email_validator(post_data['email'])
    except ValidationError:
        error_message = 'Please enter a valid email address.'

    phone_validator = RegexValidator(   
        regex=r'^\d{10}$',
        message="Please enter a valid 10-digit phone number."
    )
    try:
        phone_validator(post_data['phone'])
    except ValidationError as e:
        error_message = str(e)

    if not post_data['username']:
        error_message = "Please enter your Username!"
    elif len(post_data['username']) < 3:
        error_message = "Username must be at least 3 characters long."
    elif len(post_data['username']) >  15:
        error_message = "Username must be no more than  15 characters long."

    return error_message



def generate_otp(length=6):
    otp = ''.join(random.choices(string.digits, k=length))
    return otp

def send_otp_email(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP for email verification is: {otp}'
    from_email = 'shinasaman07@gmail.com'  
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    



def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        if entered_otp == session_otp:
            # new_email = request.session.get('new_email')

            user = request.user
            user_data = request.session.get('user_data')
            user.username = user_data['username']
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.email = user_data['email']
            user.phone = user_data['phone']
            user.save()
            del request.session['otp']
            del request.session['new_email']
            del request.session['user_data']
            return redirect('user_profile')
        else:
            messages.error(request,'OTP is invalid')
    return render(request,'email_otp_verification.html')

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            user = get_object_or_404(Customer, pk=request.user.pk)
            if user.check_password(old_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password changed successfully.')
                    return redirect('user_profile')
                else:
                    messages.error(request, 'New passwords do not match.')
            else:
                messages.error(request, 'Invalid old password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ChangePasswordForm()
    return render(request, 'change_password.html', {'form': form})

# <!-- address_list -->

def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request,'address.html',{'addresses':addresses})


def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('address_list')
    else:
        form = AddressForm()
    return render(request,'add_address.html',{'form':form})

def edit_address(request,address_id):
    address = Address.objects.get(pk=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST,instance=address)
        if form.is_valid():
            form.save()
            return redirect('address_list')
    else:
        form = AddressForm(instance=address)
    return render(request, 'edit_address.html',{'form':form})


def delete_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id)
    address.delete()
    return redirect('address_list')


# @login_required
# def order_history(request):

#     order_details = OrderProduct.objects.filter(order__user=request.user)
#     print(order_details)

#     orders = Order.objects.filter(user=request.user)
#     for o in orders:
#         print(o.address.address)
#     order_total = sum(order.payment.amount for order in orders)
#     print(order_total)
#     print(orders)

#     context = {
#         'orders': orders,
#         'order_total': order_total,
#     }
#     return render(request, 'order_history.html',context)



@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request,'order_history.html',{'orders':orders})



# @login_required
# def order_history(request):
#     orders = Order.objects.filter(user=request.user).select_related('address', 'payment')
#     order_details = []
#     for order in orders:
#         order_products = OrderProduct.objects.filter(order=order)
#         products = []
#         total_price = 0
#         for op in order_products:
#             product = Product.objects.get(id=op.product.id)
#             total_price += product.price * op.quantity
#             products.append({
#                 'name': product.product_name,
#                 'quantity': op.quantity,
#                 'price': product.price,
#             })
#         order_details.append({
#             'order': order,
#             'products': products,
#             'total_price': total_price,
#         })
#         print(order_details) # Add this line to debug
#     context = {
#         'order_details': order_details,
#     }
#     return render(request, 'order_history.html', context)


# Search

def search_results(request):

    query = request.GET.get('query')
    
    if query:
        request.session['search_query'] = query
        products  = Product.objects.filter(product_name__icontains=query)
    else:
        saved_query = request.session.get('search_query')
        if saved_query:
                # Use the saved query to fetch products
            products = Product.objects.filter(product_name__icontains=saved_query['query'])
          
            del request.session['search_query']
        else:
            products = Product.objects.all()
                

    return render(request, 'search_result.html', {'products': products, 'query': query})





def search_results_price(request):
    sort_by = request.GET.get('sort_by')
    query = request.session.get('search_query')
    print(query)

    products = Product.objects.all() 
    if query:
        products = Product.objects.filter(product_name__icontains=query)

    if sort_by == 'popularity':
        pass
    elif sort_by == 'price_low_to_high':
        products = Product.objects.filter(product_name__icontains=query).order_by('price')
    elif sort_by == 'price_high_to_low':
        products = Product.objects.filter(product_name__icontains=query).order_by('-price')
    elif sort_by == 'average_ratings':
        pass
    elif sort_by == 'featured':
        pass
    elif sort_by == 'new_arrivals':
        time_threshold = timezone.now() - timedelta(hours=24)
        products = products.filter(created_at__gte=time_threshold)
    elif sort_by == 'aA_to_zZ':
        products =  Product.objects.filter(product_name__icontains=query).order_by('product_name')
    elif sort_by == 'zZ_to_aA':
        products = Product.objects.filter(product_name__icontains=query).order_by('-product_name')

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'search_result.html', context)