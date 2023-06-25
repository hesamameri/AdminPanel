from django import forms
from .models import Ticket,TicketSystemStatus

class TicketForm(forms.ModelForm):   
    class Meta:
        model = Ticket
        fields = ['obj_source_type', 'category', 'type','source','family','address','summary','body','files','status','priority','flag']

