from datetime import timezone
import datetime
from django.shortcuts import redirect, render
from django.db.models import F
from django.utils import timezone
from customer.templatetags.converter_tags import subtract
from ticket.models import Ticket
from .models import CreditSumSVA, DepoSend, Factor, FactorAddress, FactorPayway, ObjItem, ObjItemSpec, ObjPayment, ObjSend, ObjSpec, PreFactor, VendorBuyerSVA, VendorBuyerSubSVA
from .models import CustomerSubSVA, CustomerSva, FactorComment, FactorDocument, FactorItem, FactorSVA, ObjItemSVA, ShopCustomerCount
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from Administrator.permissions import permission_required
from django.db.models import Max
from customer import models
from .models import  Inquiry  # Import your models
from django.contrib.sessions.models import Session
from django.views.decorators.cache import cache_page
from django.db.models import F, Sum
from .models import FactorItem,FactorItemBalanceSVA
from .forms import NewInquiry, NewObjItem,NewObjItemSpec
# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL', 'ROLE_ADMIN')
def customer_index(request):

    customers = CustomerSva.objects.filter(obj_item_id__gt = 10301238).order_by('obj_item_id')
    page = customers
    customer_ids = customers.values_list('obj_item_id', flat=True)
    print(customer_ids)
    # Retrieve related objects based on customer_ids
    obj_payments = ObjPayment.objects.filter(obj_item_id__in=customer_ids)
    print(obj_payments)
    tickets = Ticket.objects.filter(obj_source_id__in=customer_ids) # assuming obj_source_id is the relevant field in Ticket model
    print(tickets)
    pre_factors = PreFactor.objects.filter(buyer_id__in=customer_ids)
    print(pre_factors)
    factors = Factor.objects.filter(buyer__obj_item_id__in=customer_ids, reg_status='CONFIRM')
    print(factors)
    banks = ObjItem.objects.filter(obj_item_id__gte=999003010, obj_item_id__lte=999003019)        # Set the number of records to display per page

    # # Set the number of records to display per page
    # records_per_page = 8000
    # print(page[0].address)
    # # Initialize the Paginator object with the data and the number of records per page
    # paginator = Paginator(customers, records_per_page)

    # # Get the current page number from the request's GET parameters. If not provided, default to 1.
    # page_number = request.GET.get('page', 1)

    # try:
    #     # Get the Page object for the requested page number
    #     page = paginator.page(page_number)
    # except EmptyPage:
    #     # If the requested page number is out of range, display the last page
    #     page = paginator.page(paginator.num_pages)
    
    context = {
        'page': page,
        'obj_payments': obj_payments,
        'tickets': tickets,
        'pre_factors': pre_factors,
        'factors': factors,
        'banks':banks,
    }
    

    return render(request, 'Customer/CustomerIndex.html', context=context)

# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def new_customer(request):
    if request.method == 'POST':
        print(dict(request.POST.items()))
        obj_id = 10301
        obj_item_data = {
            'obj_id': 10301,
            'name': request.POST.get('name'),
            'title': request.POST.get('title'),
        }
        obj_specs = ObjSpec.objects.filter(obj = obj_id)
        # obj_item_spec_data = {
        #     'field1': request.POST.get('field1'),
        #     'field2': request.POST.get('field2'),
        # }
        formObjItem = NewObjItem(obj_item_data)
        if formObjItem.is_valid():
            saved_instance = formObjItem.save()


        for key, value in request.POST.items():
            # print(key,value)
        # Filter obj_specs by name attribute matching the key
            matching_spec = obj_specs.filter(name=key).first()
            print(matching_spec)
            if matching_spec:
                print(value)
                # Create a new ObjItemSpec object
                ObjItemSpec.objects.create(
                    obj_spec=matching_spec, # Use the actual object, not just its ID
                    obj_item=saved_instance, # Use the actual object, not just its ID
                    val=value
                    # ... other required fields ...
                )
        
        return redirect('customer:customerindex')

        # formObjItemSpec = NewObjItemSpec(obj_item_spec_data)
        # if formObjItemSpec.is_valid():
        #     formObjItemSpec.save()
    else:
        last_item = CustomerSva.objects.last().city_id
        print(last_item)
        return redirect('customer:customerindex')

# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_index_all(request):
    if request.method == 'POST':
        post_data = {
            'buyer': request.POST.get('buyer'),
            'first_control': 1,
            'bank': request.POST.get('bank'),
            'bank_branch': request.POST.get('bank_branch'),
            'bank_code': request.POST.get('bank_code'),
            'account_owner': request.POST.get('account_owner'),
            'account_owner_nat_code': request.POST.get('account_owner_nat_code'),
            'account_no': request.POST.get('account_no'),
            'account_shaba': request.POST.get('account_shaba'),
            'cheque_image': request.POST.get('cheque_image'),
            'cheque_price': request.POST.get('cheque_price'),
            'cheque_count': request.POST.get('cheque_count'),
            'description': request.POST.get('description'),
            'account_sayadi': request.POST.get('account_sayadi'),
            'account_sayadi': request.POST.get('account_sayadi'),
            'register': request.POST.get('register'),
            'reg_dt': datetime.datetime.now()

        }
        print(post_data)
        formInquiry = NewInquiry(post_data)
        if formInquiry.is_valid():
            saved_instance = formInquiry.save()
            print("this is true")
            return redirect('customer:customerindexAll')
        else:
            return " wrong"
    else:

        # Get distinct obj_item_ids with maximum values for each field
        distinct_records = CustomerSva.objects.all()
        
        banks = ObjItem.objects.filter(obj_item_id__gte=999003010, obj_item_id__lte=999003019)        # Set the number of records to display per page
        records_per_page = 100
        
        # Initialize the Paginator object with the data and the number of records per page
        paginator = Paginator(distinct_records, records_per_page)

        # Get the current page number from the request's GET parameters. If not provided, default to 1.
        page_number = request.GET.get('page', 1)

        try:
            # Get the Page object for the requested page number
            page = paginator.page(page_number)

        except EmptyPage:
            # If the requested page number is out of range, display the last page
            page = paginator.page(paginator.num_pages)

        context = {
            'page': page,
            'banks':banks,
            'paginator': paginator,

        }
       
        return render(request, 'Customer/CustomerIndexAll.html', context=context)



@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def new_factor(request):
    pass




@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factor(request,factor_id=None):
    if request.method == 'POST':
        pass
    else:
        if factor_id:
            factor_main = Factor.objects.get(factor_id = factor_id)
            factor_payway = FactorPayway.objects.filter(factor = factor_id)
            factor_address = FactorAddress.objects.get(factor = factor_id)
            factor_document = FactorDocument.objects.filter(factor = factor_id)
            factor_comment = FactorComment.objects.filter(factor_id = factor_id)
            # inquiry = Inquiry.objects.filter(buyer_id = factor_main.buyer_id)
            factor_item = FactorItem.objects.filter(factor= factor_id)
            factor_item_ids = factor_item.values('factor_item_id')
            factor_depo_data = DepoSend.objects.filter(depo_send_id__in = factor_item_ids)
            goods = factor_depo_data.values('goods')
            depo_ids = factor_depo_data.values('depo_id')
            combined_depo_goods_data = ObjItem.objects.filter(obj_item_id__in = goods).values('name')
            combined_depo_id_data = ObjItem.objects.filter(obj_item_id__in = depo_ids).values('name')
            combined_all_depo = list(zip(combined_depo_goods_data,combined_depo_id_data))
            depo_all = list(zip(factor_depo_data, combined_all_depo))
            obj_sendings = ObjSend.objects.filter(source_id__in = factor_item_ids)
            # factor_main_sva = FactorSVA.objects.get(factor = 64)
            context = {
                'factor_main':factor_main,
                'factor_payway':factor_payway,
                'factor_address': factor_address,
                'factor_document': factor_document,
                'factor_comment': factor_comment,
                'factor_item': factor_item,
                'depo_all':depo_all,
                'obj_sendings':obj_sendings,
            }  
            print(obj_sendings)
            return render(request,'Customer/Factor.html',context=context)
        else:
            Factor.objects.create()

# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factor_index(request):

    factor_sva_objects = FactorSVA.objects.all() 
    context = {
        'factor_sva_objects': factor_sva_objects
        }

    return render(request,'Customer/FactorList.html',context=context)



# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_confirm_accountlist(request):
    vendor_customers = FactorItemBalanceSVA.objects.filter(sended__lt=F('amount'))    
    vendor_paths = vendor_customers.values('factor_id')
    vendor_snatch = FactorItem.objects.filter(factor_item_id__in = vendor_paths)
    vendor_credit = CreditSumSVA.objects.values('vendor_buyer_id','vendor_name','reminded')
    vendor_customers = zip(vendor_customers,vendor_snatch)
    
    context = {
        'vendor_customers':vendor_customers,
    }
    return render(request,'Customer/CustomerConfirmAccountList.html',context=context)

# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_confirm_salelist(request):

    queryset = FactorItemBalanceSVA.objects.all()
    queryfactor_ids= FactorItemBalanceSVA.objects.all().values('factor_id')
    querybuyer_ids= FactorItemBalanceSVA.objects.all().values('buyer_id')
    conf_date = Factor.objects.filter(factor_id__in = queryfactor_ids).values('acc_confirm_dt')
    conf_city = CustomerSva.objects.filter(obj_item_id__in = querybuyer_ids).values('city_id')
    cities = ObjItem.objects.filter(obj_item_id__in = conf_city)
    # print(conf_date)
    # print(conf_city)
    # print(cities)
    context = {
        'items': [(item, 1) for item in queryset],
    }


    return render(request,'Customer/CustomerConfirmSaleList.html',context = context)



@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_factor_assessment(request):
    
    return render(request,'Customer/CustomerFactorAssessment.html')


# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factor_send_index(request):
    sent_index = Factor.objects.all()
    

    context = {
        'sents':sent_index,

    }
    return render(request,'Customer/FactorSendIndex.html',context=context)


# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_payment_confirm(request):
    
    return render(request,'Customer/CustomerPaymentConfirm.html')


@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_index(request):
    
    return render(request,'Customer/ReceiptIndex.html')

@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_list(request):
    
    return render(request,'Customer/ReceiptList.html')

@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_receive(request):
    
    return render(request,'Customer/ReceiptReceive.html')


@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_send(request):
    
    return render(request,'Customer/ReceiptSend.html')

@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def credit_index(request):
    
    return render(request,'Customer/CreditIndex.html')

@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def credit_list(request):
    
    return render(request,'Customer/CreditList.html')


@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_confirm(request):
    
    return render(request,'Customer/receiptconfirm.html')


@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def prefroma(request):
    
    return render(request,'Customer/Prefroma.html')


@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customerfactor_sendassigndriver(request):
    
    return render(request,'Customer/CustomerFactorSendAssignDriver.html')

@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customerfactor_sendstatus(request):
    
    return render(request,'Customer/CustomerFactorSendStatus.html')

@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customerfactor_servicedoc(request):
    
    return render(request,'Customer/CustomerFactorServiceDoc.html')

@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_payment_confirms(request):
    inquiries = Inquiry.objects.all()

    context = {
        'inquiries': inquiries,
    }
    return render(request,'Customer/CustomerPaymentConfirms.html',context=context)

# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def index_inquiry_response(request):
    if request.method == 'POST':
        
        inquiry_number = request.POST.get('inquiry_id')
        
        if request.POST.get('submitInvoice'):
            item = Inquiry.objects.get(inquiry_id = inquiry_number)
            print("this is SSSSSSSSSSSS")
            return redirect('customer:IndexInquiryResponse')

        elif request.POST.get('markAsViewed'):
            item = Inquiry.objects.get(inquiry_id = inquiry_number)
            item.shower = request.user.user_id
            item.show_dt = timezone.now()
            item.save()
            print("TTTTTTTTTTTTTTTTT")
            return redirect('customer:IndexInquiryResponse')

        else:
            print("cooooool")
            return redirect('customer:IndexInquiryResponse')
    else:
        inquiries = Inquiry.objects.filter(shower__isnull=True) 
        # print(inquiries[0].inquiry_id)   
        buyer_ids = Inquiry.objects.values_list('buyer_id',flat=True)
        factors = Factor.objects.filter(buyer_id__in=buyer_ids)
        factor_ids = factors.values_list('factor_id')
        factor_addresses = FactorAddress.objects.filter(factor_id__in=factor_ids).values('factor','phone','mobile', 'city_id', 'address')
        combined_data = list(zip(inquiries,factor_addresses))
        context = {
            'combined_data':combined_data,
        }
        return render(request, 'Customer/IndexInquiryResponse.html', context=context)



# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def index_inquiry(request):
    if request.method == 'POST':
        print(request.POST)
        inquiry_id = request.POST.get('inquiry_id')
        if inquiry_id == '':
            print("its empty")
        inquiry = Inquiry.objects.get(pk=inquiry_id)
        inquiry.sms_inquiry = request.POST.get('sms_inquiry')
        inquiry.indirect_inquiry = request.POST.get('indirect_inquiry')
        inquiry.confirm_desc = request.POST.get('confirm_desc')
        inquiry.confirm_status = request.POST.get('confirm_status')
        inquiry.confirmer = request.user.user_id
        inquiry.confirm_dt = datetime.datetime.now()
        inquiry.save()
        # print(request.POST)
        return redirect('customer:IndexInquiryResponse')
    else:
        inquiries = Inquiry.objects.filter(confirm_status__isnull=True) 
        # print(inquiries)
        inquiry_buyer = inquiries.values('buyer') 
        # print(inquiry_buyer)  
        customer_data = CustomerSva.objects.filter(obj_item_id__in = inquiry_buyer)
        combined_data = list(zip(inquiries,customer_data))
        context = {
            'inquiries': inquiries,
            'combined_data':combined_data,
        }
        return render(request,'Customer/IndexInquiry.html',context=context)




@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factorsend_installerprint(request):
    
    return render(request,'Customer/FactorSendInstallerPrint.html')

@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factor_send_print(request):
    
    return render(request,'Customer/FactorSendPrint.html')

@cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_print(request):
    
    return render(request,'Customer/ReceiptPrint.html')