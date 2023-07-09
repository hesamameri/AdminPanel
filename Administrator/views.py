from django.shortcuts import render, redirect
from django.contrib.sessions.backends.db import SessionStore

from panel import settings
from .models import User,Role,UserRole
import random
from django.contrib.auth import authenticate, login
from django.contrib import messages
import time
from django.contrib.auth.hashers import check_password,make_password
from .utils import sms  # need to fix the sms.py file and also find a solution for the user password global
from django.contrib.auth import logout
# def login_view(request):
#     pass

# from django.contrib.auth.hashers import check_password
from .models import User

def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        # print(user)
        # print(user.is_otp)
        if user is not None:
            if user.is_otp == 1:
                # Generate and store OTP
                rand = random.randint(1000, 9999)
                request.session['user_id'] = user.user_id
                request.session['mobile'] = user.mobile
                request.session['otp'] = rand
                request.session['otp_time'] = time.time()
                user.otp = rand
                user.save()
                return redirect('/otp')

            # Log in the user
            login(request, user)
            print(request.session)
            # Redirect to home page
            return redirect('home:index')
        else:
            # Display error message
            messages.error(request, 'Invalid username or password.')
            return redirect('Administrator:login_view')
    else:
        return render(request, 'Administrator/login.html')


###############
# otp ---> This part needs to be fixed
def otp(request):
    session = SessionStore(session_key=request.session.session_key)
    otp_sess = session.get('otp')
    mobile = session.get('mobile')
    
    # message = settings.TEXT_SMS_OTP % otp_sess
    # sms.send_sms(mobile, message)

    return render(request, 'Administrator/otp.html', {})

##########################

#write a log out view
# def logout(request,user_id):

def logout_view(request):
    request.session.flush()
    logout(request)
    return redirect('Administrator:login_view')    
    

