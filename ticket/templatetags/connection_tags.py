from django import template
from Administrator.models import User,UserChart
from ..models import TicketSystemCategory,TicketComment,TicketComentRead


register = template.Library()

@register.filter
def data_extraction_Ticket_assign(ticket):
    ticket_user_data = ticket.category.assign_to
    
    if ticket_user_data is not None:
        user = User.objects.filter(user_id = ticket_user_data)
        if user[0].username:
            return user[0].name
        
    else:
        return ""
    

@register.filter    
def publisher(ticket):
    ticket_publisher = ticket.register
    if ticket_publisher is not None:
        user = User.objects.filter(user_id = ticket_publisher)
        if user[0].username:
            return user[0].name
        
    else:
        return ""
    

@register.filter    
def ticket_comment_register(register):
    user = User.objects.get(user_id = register)
    return user.name

@register.filter    
def ticket_doer_register(register):
    user = User.objects.get(user_id = register)
    return user.name

# @register.simple_tag
# def remove_duplicates(queryset):
#     return queryset.distinct()

@register.filter
def ticket_doer_change_access(ticket,request):
    if ticket.category.assign_to == None:
        item = ticket.category.chart_id
        access_ids = UserChart.objects.filter(chart = item)
        access_ids = [i.user.username for i in access_ids]
        if request.user in access_ids:
            return True
        else:
            return False
    else:
        ticket_assign_id = ticket.category.assign_to
        user_category = User.objects.get(user_id = ticket_assign_id)
        if request.user == user_category:
            return True
        else:
            return False
    


