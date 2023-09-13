from django import forms
from .models import CustomerSubSVA, Factor, Inquiry,ObjItem,ObjItemSpec,ObjSpec, PreFactor



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
            'register',
            'reg_dt',
                  ]

class NewFactor(forms.ModelForm):   
    class Meta:
        model = Factor
        fields = [
            'contract',
            'buyer',
            'factore_desc',
            'register',
            'reg_dt',
            'reg_status',
            'seller_factor_id',
            'confirmer',
            'confirm_dt',
            'depo_id',
            'sale_confirmer',
            'sale_confirm_dt',
            'acc_confirmer',
            'acc_confirm_dt',
            'acc_status',
            'acc_description',
            'receipt_doc_printer_id',
            'receipt_doc_print_dt',
            'sale_confirm_status',
            'city_id',
            'address',
            'phone',
            'mobile',
            'receiver',
            'status',
            ]
class NewPreFactor(forms.ModelForm):   
    class Meta:
        model = PreFactor
        fields = [
                'obj_item_id',
                'buyer_id',
                'amount',
                'register',
                'reg_dt',


                  ]

