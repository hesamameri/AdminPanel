from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password




# @login_required(login_url='Administrator:login_view')
def index(request):
    return render(request,'./Home/index.html',{})
