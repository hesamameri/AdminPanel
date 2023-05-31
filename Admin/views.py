from django.shortcuts import render, redirect
from django.contrib.sessions.backends.db import SessionStore

from panel import settings
from .models import User
import random
from django.contrib.auth import authenticate, login
from django.contrib import messages
import time

from .utils import sms  # need to fix the sms.py file and also find a solution for the user password global

def login_view(request):
    session = SessionStore()
    return render(request, 'Admin/login.html', {'session': session})

def login_post(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None and user.status == 1:
            if user.is_otp == 1:
                # Generate and store OTP
                rand = random.randint(1000, 9999)
                request.session['user_id'] = user.id
                request.session['mobile'] = user.mobile
                request.session['otp'] = rand
                request.session['otp_time'] = time.time()
                user.otp = rand
                user.save()
                return redirect('/otp')

            # Log in the user
            login(request, user)

            # Store session ID in the database
            user.session_id = request.session.session_key
            user.save()

            # Redirect to home page
            return redirect('/otp')
        
        # Display error message
        messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
        return redirect('/otp')
###############
# otp ---> This part needs to be fixed
def otp(request):
    session = SessionStore(session_key=request.session.session_key)
    otp_sess = session.get('otp')
    mobile = session.get('mobile')
    
    # message = settings.TEXT_SMS_OTP % otp_sess
    # sms.send_sms(mobile, message)

    return render(request, 'Admin/otp.html', {})

##########################
# from django.shortcuts import redirect, render
# from django.contrib.sessions.backends.db import SessionStore
# from django.conf import settings
# from db import DB # assuming DB is a custom module for database access

# def otp_post(request):
#     if request.method == 'POST':
#         session = SessionStore(session_key=request.session.session_key)

#         otp_sess = session.get('otp')
#         otp_send = request.POST.get('otp')

#         if int(otp_send) == int(otp_sess):
#             db = DB.getConnection()
#             user_id = session.get('user_id')
#             users = db.execute('SELECT * FROM user WHERE user_id = ? AND status = 1', [user_id])
#             session['auth'] = users
#             db.update('user', {'session_id': session.session_key}, {'user_id': users[0]['user_id']})
#             return redirect('/')
#     return render(request, 'admin/auth/otp_post.html')
# ####################

# def logout_view(request):
#     session = SessionStore()
#     session.clear()
#     return redirect('/')