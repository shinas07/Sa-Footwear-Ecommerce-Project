from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Accounts.models import Customer
from Category.models import Category
from Products.models import Product,Brand
from .form import ProductForm
from django.http import JsonResponse
from Admin_app.form import BrandForm
from Home.models import Banner
from .form import BannerForm
# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard') 
        else:
            error_message = 'Incorrect username or password.'
            # return redirect('admin_login') 
            return render(request, 'admin_login.html', {'error_message': error_message})  
    else:
        return render(request, 'admin_login.html')  

@login_required
def admin_dashboard(request):
    return render(request, 'admin_index.html')


@login_required
def admin_users(request):
    users = Customer.objects.all().order_by('id')
    print(users)
    return render(request,'admin_curd.html',{'users':users})

@login_required
def block_user(request,user_id):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(Customer,pk=user_id)
        user.is_blocked = True
        user.save()
        messages.success(request, "User blocked successfully.")
        return redirect('admin_users')

@login_required
def unblock_user(request,user_id):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(Customer,pk=user_id)
        user.is_blocked = False
        user.save()
        return redirect('admin_users')
    

@login_required    
def admin_category(request):
    categorys = Category.objects.all().order_by('id')
    return render(request, 'admin_category.html', {'categorys': categorys, 'messages': messages.get_messages(request)})

@login_required
def admin_product(request):
    products = Product.objects.all()
    return render(request,'admin_product.html',{'products':products})

@login_required
def admin_add_product(request):
    # categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Product added successfully!')
            return redirect('admin_product')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print('haai')
                    messages.error(request,f"{field} : {error}") 
                return render(request, 'admin_add_product.html', {'form': form})      
    else:
        form = ProductForm()
    return render(request, 'admin_add_product.html',{'form': form})



@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_product')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_add_product.html', {'form': form})



@login_required
def unlist_product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    product.is_available  = False
    product.save()
    return redirect('admin_product')

@login_required
def list_product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    product.is_available = True
    product.save()
    return redirect('admin_product')


@login_required
def admin_add_brand(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()  # Retrieve all categories
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_add_brand') 
    else:
        form = BrandForm()
    return render(request, 'admin_add_brand.html', {'form': form, 'categories': categories, 'brands': brands})

@login_required
def block_brand(request,brand_id):
    if request.method == 'POST':
        brand = Brand.objects.get(id=brand_id)
        brand.is_active = False
        brand.save()
        return redirect('admin_add_brand')
    

def unblock_brand(request,brand_id):
    if request.method == 'POST':
        brand = Brand.objects.get(id=brand_id)
        brand.is_active = True
        brand.save()
        return redirect('admin_add_brand')
    


@login_required
def admin_add_banner(request,baner_id):
    banners = Banner.objects.all()
    if request.method =='POST':
        brand = Brand.objects.create()
        brand.save()
    else:

        return render(request,'admin_add_banner.html',{'banners':banners})
        
@login_required
def admin_add_banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_add_banner')
    banners = Banner.objects.all()
    form = BannerForm()
    return render(request, 'admin_add_banner.html', {'banners': banners, 'form': form})

@login_required
def delete_banner(request, banner_id):
    if request.method == 'POST':
        banner = Banner.objects.get(id=banner_id)
        banner.delete()
        return redirect('admin_add_banner')

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')