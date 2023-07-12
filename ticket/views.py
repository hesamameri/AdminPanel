from django.shortcuts import render,redirect,get_object_or_404
from Administrator.models import Chart,UserChart
from ticket.models import *
import home
from django.http import HttpResponse
from Administrator.models import User,UserRole
from .forms import TicketForm,TicketUpdateForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Administrator.permissions import permission_required



@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_ADMIN')
def index_ticket_view(request):  
    user_id = User.objects.get(username = request.user)
    user_permissions = UserRole.objects.filter(user = user_id).values('field_role')
    user_permissions = [item['field_role'] for item in user_permissions]
    categories = TicketSystemCategory.objects.all()
    statuses = TicketSystemStatus.objects.all()
    users = User.objects.filter(status = 1)
    ticket_counts = {}

    for category in categories:
        ticket_counts[category] = {}
        for status in statuses:
            count = Ticket.objects.filter(category=category.ticket_system_category_id, status=status.ticket_system_status_id).count()
            ticket_counts[category][status] = count
    ticket_counts_users = {}

    for user in users:
        user_ticket_counts = {}
        for status in statuses:
            count = Ticket.objects.filter(category__assign_to=user.user_id, status=status.ticket_system_status_id).count()
            user_ticket_counts[status.name] = count
        ticket_counts_users[user] = user_ticket_counts
    context = {
        'user_permissions': user_permissions,
        'categories':categories,
        'statuses': statuses,
        'users': users,
        'ticket_counts':ticket_counts,
        'ticket_counts_users':ticket_counts_users,
    }      
                       
    return render(request,'./Ticket/indexTicket.html',context=context)

@login_required(login_url='Administrator:login_view')
def confirm_ticket_view(request):
    user_id = User.objects.get(username = request.user).user_id
    # Get the tickets associated with the categories
    tickets = Ticket.objects.filter(register=user_id).filter(status_id = 4).order_by('-reg_dt')
    context = {
        'tickets': tickets,
       
    }
    return render(request,'./Ticket/confirmTicket.html',context=context)


@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def inbox_ticket_view(request):                         
    user_id = User.objects.get(username = request.user).user_id
    user_permissions = UserRole.objects.filter(user = user_id).values('field_role')
    user_permissions = [item['field_role'] for item in user_permissions]
    tickets = Ticket.objects.filter(doer = user_id).order_by('-reg_dt')
    context = {
        'tickets' : tickets,
        'user_permissions': user_permissions,
    }
    return render(request,'./Ticket/inboxTicket.html',context=context)

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def new_ticket_view(request):
    
    if request.method =='POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_ticket = Ticket.objects.create(system_id= 1, category=data['category'],type=data['type'],obj_source_type=data['obj_source_type'],
                                               family = data['family'],summary = data['summary'],body = data['body'],phone = data['phone'],phone2 = data['phone2'],
                                               files = data['files'],address = data['address'],source = data['source'],status= TicketSystemStatus.objects.get(ticket_system_status_id=1),
                                                 priority=TicketSystemPriority.objects.get(ticket_system_priority_id= 2),flag = 1,register = data['register'])
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
        user_id = User.objects.get(username = request.user)
        user_permissions = UserRole.objects.filter(user = user_id).values('field_role')
        user_permissions = [item['field_role'] for item in user_permissions]
        data = {
            'source': source,
            'type': type,
            'status': status,
            'category': category,
            'priority': priority,
            'city': city,
            'source_type': source_type,
            'user_permissions': user_permissions,
        }

        return render(request,'./Ticket/newTicket.html',{'data': data} )

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def organ_ticket_view(request,organ_id):
    user_id = User.objects.get(username = request.user)
    
    # Get the tickets associated with the categories
    

    tickets = Ticket.objects.filter(category_id=organ_id)
    excluded_values = [4,5,8,9]

    # Apply exclusion to the queryset based on values in one field
    tickets = tickets.exclude(status_id__in=excluded_values)
    new_tickets = tickets.filter(status_id=1).order_by('-reg_dt')
    ongoing_tickets = tickets.filter(status_id=3)
    customer_response_tickets = tickets.filter(status_id=6)
    tickets = (new_tickets|ongoing_tickets|customer_response_tickets)
    
    ticket_system_source = Ticket.objects.filter(category_id=organ_id).values('source_id')
    ticket_system_type = Ticket.objects.filter(category_id=organ_id).values('type_id')
    ticket_system_priority = Ticket.objects.filter(category_id=organ_id).values('priority_id')
    ticket_system_status = Ticket.objects.filter(category_id=organ_id).values('status_id')
    
    source = TicketSystemSource.objects.filter(ticket_system_source_id__in = ticket_system_source)
    type = TicketSystemType.objects.filter(ticket_system_type_id__in = ticket_system_type)
    priority = TicketSystemPriority.objects.filter(ticket_system_priority_id__in = ticket_system_priority)
    status = TicketSystemStatus.objects.filter(ticket_system_status_id__in = ticket_system_status)
    print(tickets)
    # Build the context for rendering the template
    context = {
        'tickets': tickets,
        'source': source,
        'type':type,
        'priority':priority,
        'status': status,
    }
    
    return render(request, 'Ticket/organTicket.html', context = context)


@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_ADMIN')
def quality_ticket_view(request):
    user_id = User.objects.get(username = request.user)
    # Get the charts associated with the user
    user_chart = UserChart.objects.filter(user_id=user_id)[0]
    users_chart_id = user_chart.chart_id
    # Get the categories associated with the charts
    categories = TicketSystemCategory.objects.filter(chart_id = users_chart_id)[0]
    
    # Get the tickets associated with the categories
    tickets = Ticket.objects.filter(category_id=categories)
    

    # Apply exclusion to the queryset based on values in one field
    tickets = tickets.filter(status_id = 5).order_by('-reg_dt')
    context = {
        'tickets':tickets,
        'categories':categories,
        
        
    }

    return render(request,'./Ticket/qualityTicket.html',context=context)

@login_required(login_url='Administrator:login_view')
def sent_ticket_view(request):

    user_id = User.objects.get(username = request.user).user_id
    tickets = Ticket.objects.filter(register = user_id).order_by('-reg_dt')
    context = {
        'tickets' : tickets,
    }
    return render(request,'./Ticket/sentTicket.html',context=context)

@login_required(login_url='Administrator:login_view')
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
        
        
        form = TicketUpdateForm(request.POST)
        
        if form.is_valid():
            # error_message = "Form is not valid."
            # return HttpResponse(error_message)
            data = form.cleaned_data
            
            for field in data:
                if field in form.changed_data:  # Update only the modified fields
                    setattr(ticket_item, field, data[field])
            print()
            if 'doer' in form.changed_data:
                ticket_doer = TicketDoer.objects.create(ticket = ticket_item,doer = form.cleaned_data['doer'])
                ticket_doer.save()
            ticket_item.save()
            # print(ticket_item.doer)

            # Redirect to the ticket view page
            url = reverse('ticket:viewTicket', args=[ticket_item.ticket_id])
            return redirect(url)
        else:
            # ... code for handling an invalid form ...
            error_message = "Form is not valid."
            # print(form.errors)
            return HttpResponse(error_message)
        
    else:
        
        ticket_item = get_object_or_404(Ticket, ticket_id=arg)
        ticket_comments = TicketComment.objects.filter(ticket_id = arg)
        ticket_doers = TicketDoer.objects.filter(ticket_id = arg).values('doer')
        user_id = User.objects.get(username = request.user)
        user_permissions = UserRole.objects.filter(user = user_id).values('field_role')
        user_permissions = [item['field_role'] for item in user_permissions]
        # print(ticket_doers)
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
            'user_permissions': user_permissions,
            
        }
       
        
        return render(request,'./Ticket/viewTicket.html',context=context)
    


    



@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_ADMIN')
def viewQuality_ticket_view(request,ticket_id):
    if request.method == 'POST':
        form_data = request.POST
        ticket_item = Ticket.objects.get(ticket_id = ticket_id)
        # Update the desired field
        ticket_item.star = form_data.get('star')
        ticket_item.save()
        return redirect('ticket:qualityTicket')

    else:

        ticket_item = Ticket.objects.get(ticket_id = ticket_id)
        ticket_doers = TicketDoer.objects.filter(ticket_id = ticket_id).values('doer').distinct()
        ticket_comments = TicketComment.objects.filter(ticket_id = ticket_id)
        user_id = User.objects.get(username = request.user)
        user_permissions = UserRole.objects.filter(user = user_id).values('field_role')
        user_permissions = [item['field_role'] for item in user_permissions]
        context = {
            'ticket': ticket_item,
            'doers' : ticket_doers,
            'comments':ticket_comments,
            'user_permissions': user_permissions,
        }

        return render(request,'./Ticket/viewTicketQuality.html',context=context)