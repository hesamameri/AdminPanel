from django import forms
from .models import Ticket,TicketSystemStatus,TicketDoer

class TicketForm(forms.ModelForm):   
    class Meta:
        model = Ticket
        fields = ['obj_source_type', 'category', 'type','source','family','address','summary','body','files','status','priority','flag','register']


class TicketUpdateForm(forms.ModelForm):   
    class Meta:
        model = Ticket
        fields = ['obj_source_type', 'category', 'type','source','family','address','summary','body','files','status','priority','doer','register']
        

# class TicketDoerForm(forms.ModelForm):
#     class Meta:
#         model = TicketDoer
#         fields = ['ticket','doer','register','reg_dt','leave_dt','leave_comment',]

