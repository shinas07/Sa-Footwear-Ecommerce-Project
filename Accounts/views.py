from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
# from .models import Customer
from django.views import View
from django.contrib.auth import authenticate,login

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        confirm_password = postData.get('confirm_password') 
        

        value = { 
            'firstname': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        }
        
        error_message = self.validateCustomer(value)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            hashed_password = make_password(password)
            customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=hashed_password)
            customer.save()  
            return redirect('UserLogin')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)
        
    def validateCustomer(self, data):
        error_message = None
        if not data['firstname']:
            error_message = "Please enter your First Name!"
        elif len(data['firstname']) < 3:
            error_message = "First Name must be at least 3 characters long."
        elif not data['last_name']:
            error_message = "Please enter your Last Name!"
        elif len(data['last_name']) < 3:
            error_message = "Last Name must be at least 3 characters long."
        elif not data['phone']:
            error_message = "Please enter your Phone Number!"
        elif len(data['phone']) < 10:
            error_message = "Phone Number must be at least 10 characters long."
        elif not data['password']:
            error_message = "Please enter a Password!"
        elif len(data['password']) < 5:
            error_message = "Password must be at least 5 characters long."
        elif not data['confirm_password']:
            error_message = "Please confirm your Password!"
        elif data['password'] != data['confirm_password']:
            error_message = "Password and Confirm Password do not match."
        elif not data['email']:
            error_message = "Please enter your Email!"
        elif len(data['email']) < 5:
            error_message = "Email must be at least 5 characters long."
        elif Customer.isExists(data['email']):
            error_message = 'Email Address Already Registered'

        return error_message
    
class UserLogin(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        postDate = request.POST
        email = postDate('email')
        password = postDate('password')

        user = authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('Home/home')
        else:
            error_message = 'Invalid email or password Pleace try agian.'
            return render(request,'accounts/login.html',{'error':error_message})
        


