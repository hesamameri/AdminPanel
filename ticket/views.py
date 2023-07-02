from django.shortcuts import render,redirect,get_object_or_404
from Administrator.models import Chart,UserChart
from ticket.models import *
import home
from django.http import HttpResponse
from Administrator.models import User
from .forms import TicketForm,TicketUpdateForm
from django.urls import reverse

def index_ticket_view(request):                             
    return render(request,'./Ticket/indexTicket.html',{})

def confirm_ticket_view(request):
    user_id = request.session.get('user_id')
    
    # Get the charts associated with the user
    user_chart = UserChart.objects.filter(user_id=user_id)[0]
    users_chart_id = user_chart.chart_id
    # Get the categories associated with the charts
    categories = TicketSystemCategory.objects.filter(chart_id = users_chart_id)[0]
    
    # Get the tickets associated with the categories
    tickets = Ticket.objects.filter(category_id=categories).filter(status_id = 4)
    context = {
        'tickets': tickets,
    }
    return render(request,'./Ticket/confirmTicket.html',context=context)

def inbox_ticket_view(request):                         
    # we want to have all the tickets that belong to the user here? its about the doer!
    # we assign the doer after the ticket has appeared in organ template and changed by the department head. the department head
    # assigns the doer for the task and in the inbox the user which has a user_id will see all the ticekts that has the doer with the number
    # corresponding to the user_id
    user_id = request.session.get('user_id')
    tickets = Ticket.objects.filter(doer = user_id).order_by('-reg_dt')
    context = {
        'tickets' : tickets,
    }
    return render(request,'./Ticket/inboxTicket.html',context=context)

def new_ticket_view(request):
    
    if request.method =='POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_ticket = Ticket.objects.create(system_id= 1, category=data['category'],type=data['type'],obj_source_type=data['obj_source_type'],
                                               family = data['family'],summary = data['summary'],body = data['body'],
                                               files = data['files'],address = data['address'],source = data['source'],status= TicketSystemStatus.objects.get(ticket_system_status_id=1),
                                                 priority=TicketSystemPriority.objects.get(ticket_system_priority_id= 2),flag = 1)
            new_ticket.save()
            # print(new_ticket)
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
    user_id = request.session.get('user_id')
    
    # Get the charts associated with the user
    user_chart = UserChart.objects.filter(user_id=user_id)[0]
    users_chart_id = user_chart.chart_id
    # Get the categories associated with the charts
    categories = TicketSystemCategory.objects.filter(chart_id = users_chart_id)[0]
    
    # Get the tickets associated with the categories
    tickets = Ticket.objects.filter(category_id=categories)
    excluded_values = [4,5,8,9]

    # Apply exclusion to the queryset based on values in one field
    tickets = tickets.exclude(status_id__in=excluded_values)
    new_tickets = tickets.filter(status_id=1)
    ongoing_tickets = tickets.filter(status_id=3)
    customer_response_tickets = tickets.filter(status_id=6)
    tickets = (new_tickets|ongoing_tickets|customer_response_tickets)
    print(new_tickets)
    print(ongoing_tickets)
    print(customer_response_tickets)

    # ticket_system_type
    # ticket_system_status
    # ticket_system_priority
    ticket_system_source = Ticket.objects.filter(category_id=categories).values('source_id')
    ticket_system_type = Ticket.objects.filter(category_id=categories).values('type_id')
    ticket_system_priority = Ticket.objects.filter(category_id=categories).values('priority_id')
    ticket_system_status = Ticket.objects.filter(category_id=categories).values('status_id')
    
    source = TicketSystemSource.objects.filter(ticket_system_source_id__in = ticket_system_source)
    type = TicketSystemType.objects.filter(ticket_system_type_id__in = ticket_system_type)
    priority = TicketSystemPriority.objects.filter(ticket_system_priority_id__in = ticket_system_priority)
    status = TicketSystemStatus.objects.filter(ticket_system_status_id__in = ticket_system_status)
    
    # Build the context for rendering the template
    context = {
        'tickets': tickets,
        'categories': categories,
        'source': source,
        'type':type,
        'priority':priority,
        'status': status,
    }
    
    return render(request, 'Ticket/organTicket.html', context = context)

def quality_ticket_view(request):
    return render(request,'./Ticket/qualityTicket.html',{})

def sent_ticket_view(request):
    user_id = request.session.get('user_id')
    tickets = Ticket.objects.filter(register = user_id).order_by('-reg_dt')
    context = {
        'tickets' : tickets,
    }
    return render(request,'./Ticket/sentTicket.html',context=context)

def view_ticket_view(request,arg):
    system_id = 1
    source = TicketSystemSource.objects.filter(system_id=system_id).order_by('orderby').values('ticket_system_source_id', 'name')
    type = TicketSystemType.objects.filter(system_id=system_id).order_by('orderby').values('ticket_system_type_id', 'name')
    status = TicketSystemStatus.objects.filter(system_id=system_id).order_by('orderby').values('ticket_system_status_id', 'name')
    category = TicketSystemCategory.objects.filter(system_id=system_id).order_by('orderby').values('ticket_system_category_id', 'name')
    priority = TicketSystemPriority.objects.filter(system_id=system_id).order_by('orderby').values('ticket_system_priority_id', 'name')
    doers = User.objects.all()
    ticket_item = get_object_or_404(Ticket, ticket_id=arg)
    
    if request.method == 'POST':
        
        # print("Ticket item")
        
        form = TicketUpdateForm(request.POST)
        print(form.is_valid())
        # print(form.errors)
        if form.is_valid():
            # error_message = "Form is not valid."
            # return HttpResponse(error_message)
            data = form.cleaned_data

            for field in data:
                if field in form.changed_data:  # Update only the modified fields
                    setattr(ticket_item, field, data[field])

            ticket_item.save()

            # Redirect to the ticket view page
            url = reverse('ticket:viewTicket', args=[ticket_item.ticket_id])
            return redirect(url)
        else:
            # ... code for handling an invalid form ...
            error_message = "Form is not valid."
            print(form.errors)
            return HttpResponse(error_message)
        
    else:
        
        ticket_item = get_object_or_404(Ticket, ticket_id=arg)
        ticket_comments = TicketComment.objects.filter(ticket_id = arg)
        ticket_doers = TicketDoer.objects.filter(ticket_id = arg).values('doer').distinct()
        print(ticket_doers)
        context = {
            'ticket':  ticket_item,
            'source' : source,
            'type' : type,
            'status': status,
            'category': category,
            'priority': priority,
            'comments':ticket_comments,
            'doers' : doers,
            'ticket_doers' : ticket_doers,
            
        }
       
        
        return render(request,'./Ticket/viewTicket.html',context=context)
    


    




def viewQuality_ticket_view(request):
    return render(request,'./Ticket/viewTicketQuality.html',{})