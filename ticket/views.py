from django.shortcuts import render

# Create your views here.
def confirm_ticket_view(request):
    return render(request,'./Ticket/confirmTicket.html',{})

def inbox_ticket_view(request):
    return render(request,'./Ticket/inboxTicket.html',{})

def new_ticket_view(request):
    return render(request,'./Ticket/newTicket.html',{})

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