from django import forms
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Accounts.models import Customer
from Category.models import Category
from Products.models import Product,Brand,ProductSizeColor
from .form import ProductForm
from django.http import JsonResponse
from Admin_app.form import BrandForm
from Home.models import Banner
from .form import BannerForm,ProductSizeColorForm
from django.views import View
from Orders.models import Order, OrderProduct
# from .forms import ChangeOrderStatusForm
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
    users = Customer.objects.filter(is_staff=False).order_by('id')
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
    product_size_colors = ProductSizeColor.objects.filter(is_unlisted=False)
    context = {
        'products' : products,
        'product_size_colors' : product_size_colors

        
    }
    return render(request,'admin_product.html',context)

@login_required
def admin_add_product(request):
    # categories = Category.objects.all()
    if request.method == 'POST':
        product_form = ProductForm(request.POST,request.FILES)
        product_size_color_form = ProductSizeColorForm(request.POST)
        if product_form.is_valid():
            product = product_form.save()
            messages.success(request,'Product added successfully!')
            return redirect('admin_product')
        else:
            FIELD_NAME_MAPPING = {
                'product_name': 'Product Name',
                'description': 'Description',
                'price': 'Price',
                'category': 'Category',
                'is_available': 'Availability',
                'product_brand': 'Brand',
                'left_view_image': 'Left View Image',
                'right_view_image': 'Right View Image',
                'full_view_image': 'Full View Image',
            }
            for field, errors in product_form.errors.items():
                for error in errors:
                    field_name = FIELD_NAME_MAPPING.get(field,field)
                    messages.error(request, f"{field_name } : {error}")
            return render(request, 'admin_add_product.html', {'product_form': product_form})
    else:
        product_form = ProductForm()
        return render(request, 'admin_add_product.html', {'product_form': product_form})



@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST':
        if product_form.is_valid:
            product_form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('admin_product')
        else:
            messages.error(request, 'Please correct the errors below.')
    return render(request, 'admin_edit_product.html', {'product_form': product_form,})



@login_required
def edit_product_size_color(request, pk):
    if pk:
        product = get_object_or_404(Product, id=pk)
        queryset = ProductSizeColor.objects.filter(product=product)
        ProductSizeColorFormSet = forms.modelformset_factory(ProductSizeColor, form=ProductSizeColorForm, extra=0)
        if request.method == 'POST':
            formset = ProductSizeColorFormSet(request.POST, queryset=queryset)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Product size and color updated successfully!')
                return redirect('admin_product')
            else:     
                print(formset.errors)  # Debugging: Print formset errors
                messages.error(request, 'Please correct the errors below.')
   
        else:
            formset = ProductSizeColorFormSet(queryset=queryset)
        return render(request, 'admin_edit_product_size_color.html', {'formset': formset})
    else:
        messages.error(request, 'Product ID is required.')
        return redirect('admin_product')




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
def product_size_color(request):
    if request.method == 'POST':
        form = ProductSizeColorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product size and color added successfully!')
            return redirect('admin_product')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductSizeColorForm()
    return render(request, 'admin_product_size_color.html', {'form': form})





@login_required
def admin_add_brand(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()  
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('brand_name')

            if Brand.objects.filter(brand_name=name).exists():
                messages.error(request,'Brand already exsists.')
            else:
                form.save()
                messages.success(request, 'Brand added successfully.')
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
    
@login_required
def unblock_brand(request,brand_id):
    if request.method == 'POST':
        brand = Brand.objects.get(id=brand_id)
        brand.is_active = True
        brand.save()
        return redirect('admin_add_brand')
    
@login_required
def edit_brand(request,brand_id):
    brand = get_object_or_404(Brand, id=brand_id) 
    
    if request.method == 'POST':
        form = BrandForm(request.POST,request.FILES,instance=brand)
        if form.is_valid():
            form.save()
            return redirect('admin_add_brand')
        else:
            messages.error(request, 'Error updating brand. Please check it correctly.')
    else:
        form = BrandForm(instance=brand)
    return render(request,'admin_edit_brand.html',{'form':form,'brand':brand})



#  List orders

# def admin_order_management(request):
#     if request.method == 'POST':
#         order_id = request.POST.get('order_id')
#         action = request.POST.get('action')

#         if action in dict(Order.ORDER_STATUS_CHOICES):
#             new_status = action
#             order = get_object_or_404(Order, id=order_id)
#             order.status = new_status
#             order.save()
#             messages.success(request,f"order status updated to '{new_status}' succesfully.")


#         return redirect('admin_order_management')

#     orders = Order.objects.all()
#     return render(request, 'manage_order.html', {'orders': orders})


def admin_order_management(request):
    orders = Order.objects.all()
    return render(request, 'manage_order.html', {'orders': orders})

def order_products_details(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    order_products = order.orderproduct_set.all()
    return render(request, 'manage_order_details.html', {'order': order, 'order_products': order_products})



def admin_product_status(request, order_id, order_product_id):
    order_product = get_object_or_404(OrderProduct, id=order_product_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        if new_status:
            order_product.status = new_status
            order_product.save()
            return redirect("admin_order_management")

    return redirect("admin_order_management") 
        



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