from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout



class BlockCheckMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        response = self.get_response(request)
        if request.user.is_authenticated and request.user.is_blocked:
            logout(request)
            return redirect(reverse('Accounts:login'))
        return response