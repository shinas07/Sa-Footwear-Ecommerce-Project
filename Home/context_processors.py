from Category.models import Category
from django.shortcuts import render

def categories(request):
    categories = Category.objects.filter(is_listed=True)
    return {'categories': categories}