from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Accounts.models import Customer
from Category.models import Category

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
def user_list(request):
    users = Customer.objects.all()
    return render(request,'admin_curd.html',{'users':users})

@login_required
def block_user(request,user_id):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(Customer,pk=user_id)
        user.is_blocked = True
        user.save()
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
    categorys = Category.objects.all()
    return render(request,'admin_category.html',{'categorys':categorys})

















def admin_logout(request):
    logout(request)
    return redirect('admin_login')