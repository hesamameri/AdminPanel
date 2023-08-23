from django import forms
from .models import CustomerSubSVA,ObjItem,ObjItemSpec,ObjSpec



class NewObjItem(forms.ModelForm):   
    class Meta:
        model = ObjItem
        fields = ['name','title']

class NewObjItemSpec(forms.ModelForm):   
    class Meta:
        model = ObjItemSpec
        fields = ['val']