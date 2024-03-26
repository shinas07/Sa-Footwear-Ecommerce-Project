from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from Admin_app.models import ProductOffer
from Home.forms import ChangePasswordForm,AddressForm
from .models import CancelOrder, Customer, Wallet
from django.contrib.auth.forms import PasswordChangeForm
from Products.models import Product,Category,Brand
from Category.models import Category
from Home.models import Banner,Address
from django.db.models import Q
from django.core.mail import send_mail
# from allauth.socialaccount.models import SocialApp
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
from Orders.models import  OrderProduct,Order
# from Products.models import ProductSizeColor
from django.db.models import F
from django.db.models import Q
from django.urls import reverse
from decimal import Decimal
from django.views.decorators.cache import never_cache
from django.db import IntegrityError
from django.http import JsonResponse

def home(request):
    active_category = 'home'

    # Delete expired product offers
    expired_offers = ProductOffer.objects.filter(end_date__lt=timezone.now().date())
    expired_offers.delete()

    products = Product.objects.filter(Q(category__category_name="Men") | Q(category__category_name='Women'),
        category__is_listed=True,is_available=True)
    lasted_categories = Product.objects.exclude(Q(category__category_name='Men') | Q(category__category_name='Women'))
    banners = Banner.objects.all()
    categorys = Category.objects.filter(is_listed=True)
    brands = Brand.objects.filter(is_active=True)
    context = {
        'products':products,
        'lasted_categories' :lasted_categories,
        'banners' : banners,
        'categorys':categorys,
        'active_category' : active_category,
        'brands' : brands,
    }
    return render(request, 'home.html',context)




@never_cache
def home_filter(request):
    categories = request.GET.getlist('category')
    prices = request.GET.getlist('price')
    brand_ids = request.GET.getlist('brands')
    products = Product.objects.all()
    banners = Banner.objects.all()
    categorys = Category.objects.filter(is_listed=True)
    brands = Brand.objects.filter(is_active=True)
    if categories and all(categories):
        products = products.filter(category__in=categories)
    if prices:
        for price_range in prices:
            min_price, max_price = map(int, price_range.split('-'))
            products = products.filter(price__range=(min_price, max_price))
    if brand_ids: 
        products = products.filter(product_brand__id__in=brand_ids) 
    
    no_results = not products.exists()
    context = {
        'products':products,
        'banners':banners,
        'categorys':categorys,
        'brands' : brands,
        'no_results':no_results,
        
    }
    return render(request, 'home.html', context)

#USER PROFILE
@login_required(login_url='Accounts:login')
def user_profile(request):
    user = request.user
    return render(request,'user_profile.html',{'user':user})


@login_required(login_url='Accounts:login')
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
            try:
                user.save()
                messages.success(request, 'User details updated successfully!')
                return redirect('user_profile')
            except IntegrityError as e:
                if 'duplicate key value violates unique constraint' in str(e):
                    error_message = 'Username already exists. Please choose a different username.'
                    return render(request, 'edit_profile.html', {'error': error_message, 'user': user})
                else:
                    error_message = 'An error occurred while updating user details. Please try again.'
                    return render(request, 'edit_profile.html', {'error': error_message, 'user': user})
                
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

    if not post_data['username'].strip():
        error_message = "Please enter your Username!"
    elif len(post_data['username']) < 3:
        error_message = "Username must be at least 3 characters long."
    elif len(post_data['username']) >  15:
        error_message = "Username must be no more than  15 characters long."
    elif Customer.objects.exclude(username=post_data['username']).filter(username=post_data['username']).exists():
        error_message = "Username already exists. Please choose a different one."


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
                    return redirect('Accounts:login')
                else:
                    messages.error(request, 'New passwords do not match.')
            else:
                messages.error(request, 'Invalid old password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ChangePasswordForm()
    return render(request, 'change_password.html', {'form': form})


# <!-- USER ADDRESS DETAILS -->
@login_required(login_url='Accounts:login')
def address_list(request):
    user_id = request.user.id
    addresses = Address.objects.filter(Q(user_id=user_id) & Q(is_delete=False))
    return render(request, 'address.html', {'addresses': addresses})


@login_required(login_url='Accounts:login')
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


@never_cache
@login_required(login_url='Accounts:login')
def edit_address(request,address_id):
    address = Address.objects.get(pk=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST,instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address has been successfully edited.')
            return redirect('address_list')
    else:
        form = AddressForm(instance=address)
    return render(request, 'edit_address.html',{'form':form})

@never_cache
@login_required(login_url='Accounts:login')
def delete_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id)
    address.is_delete = True
    address.save()
    return redirect('address_list')


# USER ORDER DETAILS
@login_required(login_url='Accounts:login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    order_status_list = []
    for order in orders:
        # For each order, get the corresponding OrderProduct and pick up its status
        order_status = OrderProduct.objects.filter(order=order).order_by('-id').first()
        order_status_list.append(order_status)
    context = {
        'orders':orders,
        'order_status_list':order_status_list,
    }
    return render(request,'order_history.html',context)



@login_required(login_url='Accounts:login')
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,'order_details.html',{'order':order})






@login_required(login_url='Accounts:login')
def cancel_product(request, order_product_id):
    response_data = {}
    order_product = get_object_or_404(OrderProduct, id=order_product_id)
    order = order_product.order

    if request.method == 'POST':
        if order.payment_method == 'Paid by Razorypay' or order_product.status == 'Delivered':
            order_product.status = 'Cancelled'
            order_product.save()

            refund_amount = order_product.quantity * order_product.product.price

            wallet = Wallet.objects.get(user=request.user)
            wallet.balance += refund_amount
            wallet.save()

            messages.success(request, 'Product Cancellation Success')
            response_data['status'] = 'success'
        elif order.payment_method == 'COD':
            order_product.status = 'Cancelled'
            order_product.save()
            messages.success(request, 'Product Cancellation Success')
            response_data['status'] = 'success'
        else:
            messages.error(request, 'Cancellation is not allowed for this order.')
            response_data['status'] = 'error'

        return JsonResponse(response_data)  # Return JSON response

    return render(request, 'cancel_product.html', {'order_product': order_product})



#admin_product_return
@login_required(login_url='Accounts:login')
def product_return(request,order_product_id):
    order_product = get_object_or_404(OrderProduct, id=order_product_id)

    if order_product.status == 'Returned':
        messages.warning(request, 'A return is already pending for this product.')
        return redirect(reverse('order_details', kwargs={'order_id': order_product.order.id}))
    
    if request.method == 'POST':
        order_product.status = 'Returned'
        order_product.delivery_date = None  # Clear delivery date when returning
        order_product.save()
        if order_product.order.payment_method == 'Paid by Razorypay':
            wallet_balance = Wallet.objects.get(user=request.user)
            wallet_balance.balance += order_product.order.total_amount
            wallet_balance.save()

        messages.success(request, 'Product returned successfully.')
        return redirect('order_history')
    
    return redirect("order_history")


#WALET
@login_required(login_url='Accounts:login')
def wallet_balance(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    refund_history = CancelOrder.objects.filter(user=request.user).order_by('-created_at')
    returned_products = OrderProduct.objects.filter(order__user=request.user, status='Returned')
    # Pass the wallet balance, refund history, and returned products to the template
    return render(request, 'user_wallet.html', {
        'wallet': wallet,
        'refund_history': refund_history,
        'returned_products': returned_products
    })







# PRODUCT REVIEW
@login_required(login_url='Accounts:login')
def submit_review_and_rating(request):
    if request.method == 'POST':
        order_product_id = request.POST.get('order_product_id')
        rating = request.POST.get('rating')
        review = request.POST.get('review')

        order_product = get_object_or_404(OrderProduct, id=order_product_id)
        # Check if the order product is delivered before allowing review submission
        if order_product.status == "Delivered":
            order_product.user = request.user
            order_product.rating = rating
            order_product.review = review
            order_product.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Product must be delivered to submit review.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})











#PRODUCT SEARCH
def search_results(request):

    query = request.GET.get('query')
    
    if query:
        request.session['search_query'] = query
        products  = Product.objects.filter(product_name__icontains=query, is_available=True, category__is_listed=True)
    else:
        saved_query = request.session.get('search_query')
        if saved_query:
                # Use the saved query to fetch products
            products = Product.objects.filter(product_name__icontains=saved_query['query'])
          
            del request.session['search_query']
        else:
            products = Product.objects.all()
                

    return render(request, 'search_result.html', {'products': products, 'query': query})




def search_filter_result(request):
    sort_by = request.GET.get('sort_by')
    query = request.session.get('search_query')
    products = Product.objects.all() 
    if query:
        products = Product.objects.filter(product_name__icontains=query)


    if sort_by == 'popularity':
        pass
    elif sort_by == 'price_low_to_high':
        products = Product.objects.filter(product_name__icontains=query,is_available=True, category__is_listed=True).order_by('price')
    elif sort_by == 'price_high_to_low':
        products = Product.objects.filter(product_name__icontains=query,is_available=True, category__is_listed=True).order_by('-price')
    elif sort_by == 'average_ratings':
        pass
    elif sort_by == 'featured':
        pass
    elif sort_by == 'new_arrivals':
        time_threshold = timezone.now() - timedelta(hours=24)
        products = products.filter(created_at__gte=time_threshold,is_available=True, category__is_listed=True)
    elif sort_by == 'aA_to_zZ':
        products =  Product.objects.filter(product_name__icontains=query,is_available=True, category__is_listed=True).order_by('product_name')
    elif sort_by == 'zZ_to_aA':
        products = Product.objects.filter(product_name__icontains=query,is_available=True, category__is_listed=True).order_by('-product_name')
    elif sort_by == 'Hide_out_of_stock':
        products = Product.objects.filter(productsizecolor__Stock__gt=0,product_name__icontains=query,is_available=True, category__is_listed=True)

    if sort_by == 'Hide_out_of_stock' and not products.exists():
        no_stock_message = "There are no products out of stock."
    else:
        no_stock_message = None

    context = {
        'products': products,
        'query': query,
        'no_stock_message': no_stock_message,  
    }
    return render(request, 'search_result.html', context)

def about_page(request):
    return render(request,'about.html')