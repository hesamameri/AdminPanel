from django.shortcuts import render,redirect
from ticket.models import Ticket, TicketSystemSource, TicketSystemType, TicketSystemStatus, TicketSystemCategory, TicketSystemPriority, TicketSystemCity
import home
from .forms import TicketForm
def index_ticket_view(request):
    return render(request,'./Ticket/indexTicket.html',{})

def confirm_ticket_view(request):
    return render(request,'./Ticket/confirmTicket.html',{})

def inbox_ticket_view(request):
    
    return render(request,'./Ticket/inboxTicket.html',{})

def new_ticket_view(request):
    if request.method =='POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_ticket = Ticket.objects.create(system_id= 1, category=data['category'],type=data['type'],obj_source_type=data['obj_source_type'],
                                               family = data['family'],summary = data['summary'],body = data['body'],
                                               files = data['files'],address = data['address'],source = data['source'])
            new_ticket.save()
            print(new_ticket)
            return redirect('home:index')
        
    else:

        system_id = 1
        source = TicketSystemSource.objects.filter(system_id=system_id).order_by('orderby').values('ticket_system_source_id', 'name')
        type = TicketSystemType.objects.filter(system_id=system_id).order_by('orderby').values('ticket_system_type_id', 'name')
        status = TicketSystemStatus.objects.filter(system_id=system_id).order_by('orderby').values('ticket_system_status_id', 'name')
        category = TicketSystemCategory.objects.filter(system_id=system_id).order_by('orderby').values('ticket_system_category_id', 'name')
        priority = TicketSystemPriority.objects.filter(system_id=system_id).order_by('orderby').values('ticket_system_priority_id', 'name')
        city = TicketSystemCity.objects.filter(system_id=system_id).values('ticket_system_city', 'system')
        source_type = [
            {'id': 'TOHI', 'name': ''},
            {'id': 'CUSTOMER', 'name': 'مشتری'},
            {'id': 'PERSONEL', 'name': 'پرسنل'},
            # {'id': 'BUYSELL', 'name': 'تامین کنندگان'},
            # {'id': 'USERS', 'name': 'کاربران سیستم'},
            {'id': 'TICKETCUSTOMER', 'name': 'متفرقه'},
        ]
        
        data = {
            'source': source,
            'type': type,
            'status': status,
            'category': category,
            'priority': priority,
            'city': city,
            'source_type': source_type,
        }

        return render(request,'./Ticket/newTicket.html',{'data': data} )

def organ_ticket_view(request):
    return render(request,'./Ticket/organTicket.html',{})

def quality_ticket_view(request):
    return render(request,'./Ticket/qualityTicket.html',{})

def sent_ticket_view(request):
    return render(request,'./Ticket/sentTicket.html',{})

def view_ticket_view(request):
    return render(request,'./Ticket/viewTicket.html',{})

def viewQuality_ticket_view(request):
    return render(request,'./Ticket/viewTicketQuality.html',{})