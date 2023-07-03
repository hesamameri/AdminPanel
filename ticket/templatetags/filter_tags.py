from django import template
from Administrator.models import User
from ..models import TicketSystemCategory
import re

register = template.Library()

@register.filter
def None_fix(ticket_item):
    if ticket_item == None:
        return ' '
    else:
        return ticket_item
    
@register.filter
def html_fix(todo):
    if todo != None:
        body = todo.body
        if body != None:
            clean_body =  re.sub('<.*?>', '', body)
            clean_text = re.sub('&\w+;', '', clean_body)
            return clean_text
        
    else:
        return "ok"

@register.filter
def turn_service(star):
    star_score = {1:'بد' ,2:'متوسط',3:'خوب',4:'عالی'}
    return star_score[star]