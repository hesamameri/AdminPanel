from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Administrator.models import User,UserRole,UserChart
from ticket.models import Ticket,TicketSystemCategory

@login_required(login_url='Administrator:login_view')
def index(request):
   
    return render(request,'./Home/index.html',{})
