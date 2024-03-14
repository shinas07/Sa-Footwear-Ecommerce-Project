from urllib import request
from django.shortcuts import render,redirect,get_object_or_404
from .models import Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
from django.db.models import Q
from django.views.decorators.cache import never_cache

@never_cache
@login_required
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name').strip()
        description = request.POST.get('category_description').strip()
        if not category_name:
            messages.error(request,'Category name cannot be empty.')
            return redirect('admin_category')
        if Category.objects.filter(category_name__iexact=category_name).exists():
            messages.error(request, 'Category already exists. Please choose a different name.')
            return redirect('admin_category')
        
        Category.objects.create(category_name=category_name, description=description)
        messages.success(request, 'Category added successfully!')
        return redirect('admin_category')
    else:
        return render(request, 'add_category.html')

@login_required
def list_category(request,category_id):
    category = Category.objects.get(id=category_id)
    category.is_listed = True
    category.save()
    return redirect('admin_category')

@login_required
def unlist_category(request,category_id):
    category = Category.objects.get(id=category_id)
    category.is_listed = False
    category.save()
    return redirect('admin_category')

@login_required(login_url='Accounts:login')
def edit_category(request, category_id):
    # Retrieve the category object
    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == 'POST':

        new_category_name = request.POST.get('edit_category_name')

        if Category.objects.filter(Q(category_name__iexact=new_category_name) & ~Q(pk=category_id)).exists():
            messages.error(request, 'Category already exists. Please choose a different name.')
            return redirect('admin_category')
        category.category_name = request.POST.get('edit_category_name')
        category.description = request.POST.get('edit_category_description')
        category.save()
        
        # Redirect back to the admin category page after editing
        return redirect('admin_category')
    
    return render(request, 'admin_base.html')
