from django.shortcuts import render

# Create your views here.

def create_category():
    if request.method == 'POST':
        category_name = request.POST.get('catergory_name')
        description = request.POST.get('descrption')
        
