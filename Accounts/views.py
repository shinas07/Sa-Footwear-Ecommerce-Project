
from django.http import JsonResponse
from django.shortcuts import render, redirect , HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
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
from django.contrib.auth.hashers import check_password
import re
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator,RegexValidator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
        # entered_otp = postData.get('otp') 
        

        value = { 
            'username' :username,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        }
   
        error_message = self.validateCustomer(value)

        if not error_message:

            otp = generate_otp()
            request.session['signup_data'] = {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'email': email,
                'password': password,
                'otp' : otp,
            }
            
            send_otp_email(email,otp)
            return redirect('Accounts:signup_verify_otp')

              
        else:
     
            data = {
            
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)
        
    def validateCustomer(self, data):
        error_message = None

        email_validator = EmailValidator()
        try:
            email_validator(data['email'])
        except ValidationError:
            error_message = 'Pleace enter a valid Email address.'

        phone_validator = RegexValidator(   
            regex=r'^\d{10}$',
            message="Please enter a valid Indian phone number."
            )
        try:
            phone_validator(data['phone'])
            if data['phone'] == '0000000000':  
                raise ValidationError("Phone number cannot be all zeros.")
        except ValidationError as e:
            error_message = str(e)

        try:
            phone_validator(data['phone'])
        except ValidationError:
            error_message = "Please enter a valid Phone number."

        if not data['username']:
            error_message = "Please enter your Username!"
        elif len(data['username']) < 3:
            error_message = "Username must be at least 3 characters long."
        elif len(data['username']) >  10:
            error_message = "Username must be no more than  10 characters long."
        elif Customer.objects.filter(username=data['username']).exists():
            error_message ='Username is already taken.'
        elif not data['first_name']:
            error_message = "Please enter your First Name!"
        elif len(data['first_name']) < 3:
            error_message = "First Name must be at least 3 characters long."
        elif not data['last_name']:
            error_message = "Please enter your Last Name!"
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
        elif Customer.objects.filter(email=data['email']).exists():
            error_message = 'Email Address Already Registered'
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            error_message = "Invalid Email Address"

        return error_message
    
    def SignupOtp(request,email):
        otp = generate_otp()
        request.sesstion['otp'] = otp
        send_otp_email(email,otp)



class SignUpVerifyOTP(View):
    def get(self, request):
        return render(request, 'verify_signupOtp.html')

    def post(self, request):
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('signup_data').get('otp')
        email = request.session.get('signup_data').get('email')

        if entered_otp == session_otp:
            signup_data = request.session.get('signup_data')
            hashed_password = make_password(signup_data['password'])
            customer = Customer(username=signup_data['username'], first_name=signup_data['first_name'],
                                last_name=signup_data['last_name'], phone=signup_data['phone'],
                                email=signup_data['email'], password=hashed_password)
            customer.save()

            del request.session['signup_data']

            messages.success(request, 'User registered successfully!')
            return redirect('Accounts:login')
        else:
            return render(request, 'verify_signupOtp.html', {'error': 'Incorrect OTP. Please try again.'})




    


class UserLogin(View):
    def get(self,request):
        return render(request,'login.html')     
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_blocked:
                error_message = 'Your account has been blocked. Please contact the customer care'
                return render(request,'login.html',{'error':error_message})
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid Username or password. Please try again.'
            return render(request, 'login.html', {'error': error_message})


class VerifyOTP(View):
    def get(self,request):
        return render(request,'email_verification.html')

    
    def post(self,request):
        email = request.POST.get('email')
        # email_response = self.email_verification(request, email)
        otp_entered = request.POST.get('otp')
        if self.is_valid_otp(otp_entered):
        # This block should only execute if the OTP is valid

            if 'otp' in request.session:
                del request.session['otp']
            if 'otp_expiry' in request.session:
                del request.session['otp_expiry']
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
            return redirect('Accounts:login')  
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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def resend_otp(request):
    print('hlwwww')
    if request.method == 'POST':
        signup_data = request.session.get('signup_data', {})

        otp = generate_otp()
      
        signup_data['otp'] = otp
        
     
        email = signup_data.get('email')
        
        send_otp_email(email, otp)
        

        request.session['signup_data'] = signup_data
        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




def user_logout(request):
    logout(request)
    return redirect('home')




