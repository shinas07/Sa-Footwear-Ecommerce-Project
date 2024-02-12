from urllib import request
from django.shortcuts import render,redirect
from .models import Category
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def create_category():
    if request.method == 'POST':
        category_name = request.POST.get('catergory_name')
        description = request.POST.get('descrption')
        Category.objects.create(name=category_name,description=description)
        return redirect('admin_category')
    else:
        return render(request,'add_category.html')