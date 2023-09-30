from django import forms
from .models import CustomerSubSVA, DepoSend, Factor, FactorAddress, FactorDocument, FactorItem, FactorPayway, Inquiry,ObjItem,ObjItemSpec, ObjPayment, ObjSend,ObjSpec, PreFactor



class NewObjItem(forms.ModelForm):   
    class Meta:
        model = ObjItem
        fields = ['obj','name','title']

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
            'bank_id',
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

class NewObjPayment(forms.ModelForm):   
    class Meta:
        model = ObjPayment
        fields = [
                
                'obj_item_id',
                'type',
                'source_type',
                'source_id' ,
                'price',
                'description',
                'register',
                'reg_dt',
                'bank_id',
                'branch_code',
                'no',
                'owner',
                ]

class NewFactorPayway(forms.ModelForm):
    class Meta:
            model = FactorPayway
            fields = [
                    
                    'factor',
                    'pay_level',
                    'pay_type',
                    'price' ,
                    'bank',
                    'cheque_owner',
                    'no',
                    'description',
                    'register',
                    'reg_dt',
                    
                    ]

class NewFactorItem(forms.ModelForm):
    class Meta:
            model = FactorItem
            fields = [
                    'factor',
                    'obj_item',
                    'amount',
                    'unit_price',
                    'discount_price',
                    'register',
                    ]
            
class NewFactorAddress(forms.ModelForm):
    class Meta:
            model = FactorAddress
            fields = [
                    'factor',
                    'city_id',
                    'phone',
                    'mobile',
                    'address',
                    'receiver',
                    ]
    
class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = FactorDocument
        fields = [
            'factor',
            'document_type',
            'uri',
            'description',
            'level_type',
            'register',
            'hash',
            'reg_dt',

            ]
class NewDepoSend(forms.ModelForm):
    class Meta:
            model = DepoSend
            fields = [
                    'source_type',
                    'source_id',
                    'goods',
                    'phone',
                    'mobile',
                    'address',
                    'receiver',
                    'depo_id',
                    'reg_dt',
                    'register',
                    'amount',
                    ]

class NewObjSend(forms.ModelForm):
    class Meta:
            model = ObjSend
            fields = [
                    'source_type',
                    'source_id',
                    'action',
                    ]