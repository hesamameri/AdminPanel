from django import template
from Administrator.models import User
from ..models import TicketSystemCategory


register = template.Library()

@register.filter
def None_fix(ticket_item):
    if ticket_item == None:
        return ' '
    else:
        return ticket_item


    