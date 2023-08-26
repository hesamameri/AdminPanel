from django import forms
from .models import CustomerSubSVA, Inquiry,ObjItem,ObjItemSpec,ObjSpec



class NewObjItem(forms.ModelForm):   
    class Meta:
        model = ObjItem
        fields = ['name','title']

class NewObjItemSpec(forms.ModelForm):   
    class Meta:
        model = ObjItemSpec
        fields = ['val']

class NewInquiry(forms.ModelForm):   
    class Meta:
        model = Inquiry
        fields = [
            'buyer',
            'first_control',
            'bank',
            'bank_branch',
            'bank_code',
            'account_owner',
            'account_owner_nat_code',
            'account_no',
            'account_sayadi',
            'account_shaba',
            'cheque_image',
            'cheque_price',
            'cheque_count',
            'description',
                  ]