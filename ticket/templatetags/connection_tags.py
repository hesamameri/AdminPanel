from django import template
from Administrator.models import User
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
    print("S")
    print(register)
    user = User.objects.get(user_id = register)
    print("S")
    return user.name

# @register.simple_tag
# def remove_duplicates(queryset):
#     return queryset.distinct()