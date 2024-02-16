
from django.shortcuts import render, redirect , HttpResponse
from django.contrib.auth.hashers import make_password
# from .models import Customer
from django.views import View
from django.contrib.auth import authenticate,login
import random
import string
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from Accounts.models import Customer
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        username = postData.get('username')
        first_name = postData.get('first_name')
        last_name = postData.get('last_name')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        confirm_password = postData.get('confirm_password') 
        

        value = { 
            'username' :username,
            'firstname': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        }
        print(value)
   
        error_message = self.validateCustomer(value)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            hashed_password = make_password(password)
            customer = Customer(username=username,first_name=first_name, last_name=last_name, phone=phone, email=email, password=hashed_password)
            customer.save()
            return redirect('Accounts:login')
        else:
            print(error_message)
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
        elif Customer.objects.filter(email=data['email']).exists():
            error_message = 'Email Address Already Registered'
        return error_message
    


class UserLogin(View):
    def get(self,request):
        return render(request,'login.html')
     
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        print("Email:", username)  # Debugging output
        print("Password:", password)  # Debugging output
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        print("Authenticated User:", user) 

        if user is not None:
            # Login user
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid email or password. Please try again.'
            return render(request, 'login.html', {'error': error_message})



class VerifyOTP(View):
    def get(self,request):
        return render(request,'email_verification.html')

    
    def post(self,request):
        email = request.POST.get('email')
        email_response = self.email_verification(request, email)
        otp_entered = request.POST.get('otp')
        if self.is_valid_otp(otp_entered):
        # This block should only execute if the OTP is valid

            if 'otp' in request.session:
                del request.session['otp']
            if 'otp_expiry' in request.session:
                del request.session['otp_expiry']
                print('verifed')
                return self.new_password(request)  # Call reset_password method and return its result
            else:
                error_message = 'Email or Password not found in session'
        else:
            error_message = 'Invalid OTP. Please try again'
        return render(request,'otp_verification.html',{'error':error_message})
    
    def email_verification(self, request, email):  # Define the email_verification method
        if not Customer.objects.filter(email=email).exists(): 
            error_message_email = 'Invalid email. Please use a registered email address.'
            return render(request, 'email_verification.html', {'email_error': error_message_email})
        request.session['email'] = email
        otp = generate_otp()
        send_otp_email(email, otp)
        request.session['otp'] = otp
        request.session['otp_expiry'] = calculate_expiry_time()
        return render(request, 'otp_verification.html', {'otp_expiry': request.session['otp_expiry']})
    
    def is_valid_otp(self, otp_entered):
        otp_stored = self.request.session.get('otp')
        return otp_entered == otp_stored
    
    def new_password(self, request):
        return render(request,'new_password.html')



class NewPasswordView(View):
    def get(self, request):
        return render(request, 'new_password.html')
    
    def post(self, request):
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            error_message = 'Password do not match.Pleace try again.'
            return render(request,'new_password.html',{'error':error_message})
        email = request.session.get('email')
        user = Customer.objects.filter(email=email).first()
        if user:
            hashed_password = make_password(password)
            user.password = hashed_password
            user.save()
            return redirect('Accounts:login')  # Redirect to login page after resetting password
        else:
            return render(request, 'new_password.html')


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def send_otp_email(email, otp):
    subject = 'Your OTP for Sign Up'
    message = f'Your OTP sign up is : {otp}'
    sender_email = 'SA Footwear <Sa Footwear@gmail.com>'
    send_mail(subject, message, sender_email, [email], fail_silently=False)


def calculate_expiry_time():
    expiry_time = datetime.now() + timedelta(minutes=5)
    return expiry_time.isoformat()

def resend_otp(request):
    email = request.session.get('signup_email')
    otp = generate_otp()
    send_otp_email(email,otp)
    request.session['otp'] = otp 
    request.session['otp_expiry'] = calculate_expiry_time()
    return redirect('signup')



def user_logout(request):
    logout(request)
    return redirect('home')
