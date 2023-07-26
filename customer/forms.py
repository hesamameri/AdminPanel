from django import forms
from .models import CustomerSubSVA



class NewCustomerForm(forms.ModelForm):   
    class Meta:
        model = CustomerSubSVA
        fields = []
    