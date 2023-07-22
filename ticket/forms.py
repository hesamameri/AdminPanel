from django import forms
from .models import Ticket,TicketSystemStatus,TicketDoer
from django.core.exceptions import ValidationError


class TicketForm(forms.ModelForm):   
    class Meta:
        model = Ticket
        fields = ['obj_source_type', 'category', 'type','source','family','address','summary','doer','body','files','status','priority','flag','register','phone2','phone']
    
class TicketUpdateForm(forms.ModelForm):   
    class Meta:
        model = Ticket
        fields = ['obj_source_type', 'category', 'type','source','family','address','summary','files','status','priority','doer','register']
    ticket_comment = forms.CharField(widget=forms.Textarea, required=False)

# class TicketDoerForm(forms.ModelForm):
#     class Meta:
#         model = TicketDoer
#         fields = ['ticket','doer','register','reg_dt','leave_dt','leave_comment',]

