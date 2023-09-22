from datetime import timezone
import datetime
from django.http import HttpResponse
from django.urls import reverse
from .utilities import get_object_or_none
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F
from django.utils import timezone
from customer.templatetags.converter_tags import subtract
from ticket.models import Ticket
from .models import CreditSumSVA, DepoSend, Factor, FactorAddress, FactorPayway, ObjItem, ObjItemSpec, ObjPayment, ObjSend, ObjSpec, PreFactor, ProductSVA, VendorBuyerSVA, VendorBuyerSubSVA
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
from .forms import NewFactorItem, NewFactorPayway, NewInquiry, NewObjItem,NewObjItemSpec, NewObjPayment, NewPreFactor


# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL', 'ROLE_ADMIN')
def customer_index(request):
    if request.method == 'POST':
        post_data = {
            'buyer': request.POST.get('buyer'),
            'first_control': 1,
            'bank_id': request.POST.get('bank_id'),
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
     
        formInquiry = NewInquiry(post_data)
        if formInquiry.is_valid():
            saved_instance = formInquiry.save()
            print("this is true")
            return redirect('customer:customerindex')
        else:
            return " wrong"
    else:
        customers = CustomerSva.objects.filter(obj_item_id__gt = 1030200027).order_by('obj_item_id')
        page = customers
        customer_ids = customers.values_list('obj_item_id', flat=True)
        # Retrieve related objects based on customer_ids
        obj_payments = ObjPayment.objects.filter(obj_item_id__in=customer_ids)
        # print(obj_payments)
        tickets = Ticket.objects.filter(obj_source_id__in=customer_ids) # assuming obj_source_id is the relevant field in Ticket model
        # print(tickets)
        pre_factors = PreFactor.objects.filter(buyer_id__in=customer_ids)
        # print(pre_factors)
        factors = Factor.objects.filter(buyer_id__in=customer_ids,)
        # print(factors)
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
    


@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_pay(request,factor_id=None):
    
    if request.method == 'POST':
        if factor_id is None:
            pay_type = request.POST.get('type')
            if pay_type == 'CASH':
                print(request.POST)
                pay_data = {
                'obj_item_id': request.POST.get('obj_item_id'),
                'type': request.POST.get('type'),
                'source_type': 'CUSTOMER_PAYMENT',
                'source_id': request.POST.get('obj_item_id'),
                'price': request.POST.get('price'),
                'register': request.POST.get('register'),
                'description': request.POST.get('description'),
                'reg_dt': datetime.datetime.now(),
                            }
                
                payment_form = NewObjPayment(pay_data)
                if payment_form.is_valid():
                    payment_form.save()  # Save the payment object to the database
                    return redirect('customer:customerindex')
                else:
                    print('didnt work')
                    return redirect('customer:customerindex')
                
            elif pay_type == 'CART':
                pay_data = {

                'obj_item_id': request.POST.get('obj_item_id'),
                'type': request.POST.get('type'),
                'source_type': 'CUSTOMER_PAYMENT',
                'source_id': request.POST.get('obj_item_id'),
                'price': request.POST.get('price'),
                'register': request.POST.get('register'),
                'description': request.POST.get('description'),
                'reg_dt': datetime.datetime.now(),
                'bank_id': request.POST.get('bank_id'),
                'no': request.POST.get('no'),
                'branch_code':request.POST.get('branch_code'),
                            }
                
                payment_form = NewObjPayment(pay_data)
                if payment_form.is_valid():
                    payment_instance = payment_form.save()  # Save the payment object to the database
                    return redirect('customer:customerindex')
                else:
                    print('didnt work')
                    return redirect('customer:customerindex')

            elif pay_type == 'CARTOCART':
                pay_data = {
                'obj_item_id': request.POST.get('obj_item_id'),
                'price': request.POST.get('price'),
                'register': request.POST.get('register'),
                'description': request.POST.get('description'),
                'type': request.POST.get('type'),
                'source_type': 'CUSTOMER_PAYMENT',
                'source_id': request.POST.get('obj_item_id'),
                'bank_id': request.POST.get('bank_id'),
                'no': request.POST.get('no'),
                'branch_code':request.POST.get('branch_code'),
                'reg_dt': datetime.datetime.now(),
                            }
                
                payment_form = NewObjPayment(pay_data)
                if payment_form.is_valid():
                    payment_instance = payment_form.save()  # Save the payment object to the database
                    return redirect('customer:customerindex')
                else:
                    print('didnt work')
                    return redirect('customer:customerindex')
   


            else:
                pay_data = {
                'obj_item_id': request.POST.get('obj_item_id'),
                'price': request.POST.get('price'),
                'register': request.POST.get('register'),
                'description': request.POST.get('description'),
                'type': request.POST.get('type'),
                'source_type': 'CUSTOMER_PAYMENT',
                'source_id': request.POST.get('obj_item_id'),
                'bank_id': request.POST.get('bank_id'),
                'no': request.POST.get('no'),
                'branch_code':request.POST.get('branch_code'),
                'owner': request.POST.get('owner'),
                'reg_dt': datetime.datetime.now(),
                            }
                
                payment_form = NewObjPayment(pay_data)
                if payment_form.is_valid():
                    payment_instance = payment_form.save()  # Save the payment object to the database
                    return redirect('customer:customerindex')
                else:
                    
                    return redirect('customer:customerindex')
        else:
           pass
    else:
        return redirect('customer:customerindex')

# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def new_customer(request):
    if request.method == 'POST':
        print(dict(request.POST.items()))
        obj_id = 10301

        obj_item_data = {

            'obj': 10301,
            'name': request.POST.get('name'),
            'title': request.POST.get('title'),

        }

        obj_specs = ObjSpec.objects.filter(obj = obj_id)
        print(obj_item_data)
        # obj_item_spec_data = {
        #     'field1': request.POST.get('field1'),
        #     'field2': request.POST.get('field2'),
        # }
        formObjItem = NewObjItem(obj_item_data)
        if formObjItem.is_valid():
            saved_instance = formObjItem.save()
        else:
            print("WROOOONG")

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
            'bank_id': request.POST.get('bank_id'),
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
            return "wrong"
    else:

        # Get distinct obj_item_ids with maximum values for each field
        # distinct_records = CustomerSva.objects.all()
        customers = CustomerSva.objects.filter(obj_item_id__gt = 1030200027).order_by('-obj_item_id')
        page = customers
        customer_ids = customers.values_list('obj_item_id', flat=True)
        # Retrieve related objects based on customer_ids
        obj_payments = ObjPayment.objects.filter(obj_item_id__in=customer_ids)
        print(obj_payments)
        tickets = Ticket.objects.filter(obj_source_id__in=customer_ids) # assuming obj_source_id is the relevant field in Ticket model
        print(tickets)
        pre_factors = PreFactor.objects.filter(buyer_id__in=customer_ids)
        print(pre_factors)
        factors = Factor.objects.filter(buyer_id__in=customer_ids, reg_status='CONFIRM')
        # customer_ids = distinct_records.values_list('obj_item_id', flat=True)
        # obj_payments = ObjPayment.objects.filter(obj_item_id__in=customer_ids)
        # tickets = Ticket.objects.filter(obj_source_id__in=customer_ids) # assuming obj_source_id is the relevant field in Ticket model
        # pre_factors = PreFactor.objects.filter(buyer_id__in=customer_ids)
        # factors = Factor.objects.filter(buyer_id__in=customer_ids, reg_status='CONFIRM')

        banks = ObjItem.objects.filter(obj_item_id__gte=999003010, obj_item_id__lte=999003019) 
        records_per_page = 100
        
        # Initialize the Paginator object with the data and the number of records per page
        paginator = Paginator(customers, records_per_page)

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
            'obj_payments': obj_payments,
            'tickets': tickets,
            'pre_factors': pre_factors,
            'factors': factors,

        }
       
        return render(request, 'Customer/CustomerIndexAll.html', context=context)



@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def new_factor(request):
    pass




@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factor(request,factor_id=None,obj_buyer = None):
    # print("factor_id: ", factor_id) 3757
    # print("buyer_id: ", obj_buyer)
    
    if request.method == 'POST':
        print(request.POST)
        form_type = request.POST.get('form_type')
        if form_type == 'paywayform':
            payway_data = {
                'factor': request.POST.get('factor_id'),
                'pay_level':'FACTOR',
                'pay_type':request.POST.get('pay_type'),
                'price': request.POST.get('price'),
                'bank':request.POST.get('bank_id'),
                'cheque_owner':request.POST.get('owner'),
                'no':request.POST.get('no'),
                'description':request.POST.get('description'),
                'register':request.POST.get('register'),
                'reg_dt': datetime.datetime.now(),    
            }
            paywayform = NewFactorPayway(payway_data)
            if paywayform.is_valid():
                paywayform.save()
                return  redirect(reverse('customer:FactorWithFactorID', args=[payway_data['factor']]))  # or redirect as per your needs
            else:
                # Handle the form errors. This is just a simple example.
                # You might want to send the errors back to the template or handle in some other way.
                return HttpResponse("Form has errors: {}".format(paywayform.errors))

    else:
        # try:
            if factor_id is not None:

                # factor_main = Factor.objects.get(factor_id = factor_id)
                factor_main = get_object_or_none(Factor, factor_id=factor_id)
                
                # customer_data = CustomerSva.objects.get(obj_item_id = factor_main.buyer_id)
                customer_data = get_object_or_none(CustomerSva, obj_item_id=factor_main.buyer_id)
                
                # inquiry_test = Inquiry.objects.get(buyer_id = factor_main.buyer_id)
                inquiry_test = get_object_or_none(Inquiry, buyer_id=factor_main.buyer_id)

                if customer_data.seller_buyer_id is not None:
                    credit_id = int(customer_data.seller_buyer_id[:10])
                    vendor_credit = get_object_or_none(CreditSumSVA, pk=credit_id)

                else:
                    credit_id = 102010
                    vendor_credit = None

                # vendor_credit = CreditSumSVA.objects.get(pk = credit_id)
                
                factor_payway = FactorPayway.objects.filter(factor = factor_id)

                # factor_address = FactorAddress.objects.get(factor = factor_id)
                factor_address = get_object_or_none(FactorAddress, factor=factor_id)

                factor_document = FactorDocument.objects.filter(factor = factor_id)
                factor_comment = FactorComment.objects.filter(factor_id = factor_id)
                factor_item = FactorItem.objects.filter(factor= factor_id)
                factor_item_ids = factor_item.values('factor_item_id')
                factor_depo_data = DepoSend.objects.filter(depo_send_id__in = factor_item_ids)
                goods = factor_depo_data.values('goods')
                depo_ids = factor_depo_data.values('depo_id')
                combined_depo_goods_data = ObjItem.objects.filter(obj_item_id__in = goods).values('name')
                combined_depo_id_data = ObjItem.objects.filter(obj_item_id__in = depo_ids).values('name')
                combined_all_depo = list(zip(combined_depo_goods_data,combined_depo_id_data))
                depo_all = list(zip(factor_depo_data, combined_all_depo))
                if depo_all == []:
                    depo_all = None
                
                obj_sendings = ObjSend.objects.filter(source_id__in = factor_item_ids)
                banks = ObjItem.objects.filter(obj_item_id__gte=999003010, obj_item_id__lte=999003019) 
                paywayform = NewFactorPayway()
                context = {

                    'factor_main':factor_main,
                    'customer_data':customer_data,
                    'vendor_credit':vendor_credit,
                    'factor_payway':factor_payway,
                    'factor_address': factor_address,
                    'factor_document': factor_document,
                    'factor_comment': factor_comment,
                    'factor_item': factor_item,
                    'depo_all':depo_all,
                    'obj_sendings':obj_sendings,
                    'inquiry_test':inquiry_test,
                    'banks':banks,
                    'paywayform':paywayform,

                }  
               
                
                return render(request,'Customer/Factor.html',context=context)
            else:
                print(obj_buyer)
                objinstance = ObjItem.objects.get(obj_item_id = obj_buyer)
                print(objinstance)
                new_factor = Factor.objects.create(buyer = objinstance,register = request.user.user_id,reg_dt = datetime.datetime.now())
                return redirect('customer:FactorWithFactorID', factor_id=new_factor.factor_id)
        # except:
        #     banks = ObjItem.objects.filter(obj_item_id__gte=999003010, obj_item_id__lte=999003019) 
        #     context = {
        #         'banks':banks,
        #     }
        #     return render(request,'Customer/Factor.html',context=context)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factor_add_goods(request,factor_id):
    if request.method == 'POST':
        obj_item_id = request.POST.get('obj_item')
        obj = get_object_or_404(ObjItem, obj_item_id=obj_item_id)
        factor = get_object_or_404(Factor,factor_id=factor_id)
        unit_price = get_object_or_404(ProductSVA,product_id = obj.obj_item_id).unit_price
        goods_data = {
            'factor':factor,
            'obj_item':obj,
            'amount':request.POST.get('amount'),
            'unit_price': unit_price,
            'discount_price': 1,
            'register':request.POST.get('amount'),
        }
        goodsform = NewFactorItem(goods_data)
        if goodsform.is_valid():
            goodsform.save()
            return redirect(reverse('customer:FactorWithFactorID', args=[factor_id]))  # Adjust the redirect as per your needs

        else:
            return redirect(reverse('customer:FactorWithFactorID', args=[request.POST.get('factor')]))  # Adjust the redirect as per your needs
 
        
    else:
        return redirect('customer:customerindex')

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def delete_factor_element(request,element):
    if request.method == 'POST':
        if request.POST['form_type'] == 'paywayform':
            payway = get_object_or_404(FactorPayway, pk=element)
            payway.delete()
            return redirect(reverse('customer:FactorWithFactorID', args=[request.POST.get('factor')]))  # Adjust the redirect as per your needs
        elif request.POST['form_type'] == 'addgoods':
            payway = get_object_or_404(FactorItem, pk=element)
            payway.delete()
            return redirect(reverse('customer:FactorWithFactorID', args=[request.POST.get('factor')]))
    else:
        return redirect('customer:customerindex')

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
    vendor_customers = zip(vendor_customers,vendor_snatch)
    
    context = {
        'vendor_customers':vendor_customers,
    }
    return render(request,'Customer/CustomerConfirmAccountList.html',context=context)

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_confirm_salelist(request):

    queryset = FactorItemBalanceSVA.objects.all()
    queryfactor_ids= FactorItemBalanceSVA.objects.all().values('factor_id')
    querybuyer_ids= FactorItemBalanceSVA.objects.all().values('buyer_id')
    conf_city = CustomerSva.objects.filter(obj_item_id__in = querybuyer_ids).values('obj_item_id')
    cities = ObjItem.objects.filter(obj_item_id__in = conf_city)
    remaining_credit = CreditSumSVA.objects.filter()
    context = {
        'items': [(item, 1) for item in queryset],
    }
    return render(request,'Customer/CustomerConfirmSaleList.html',context = context)



# @cache_page(10)
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


# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_index(request):
    
    return render(request,'Customer/ReceiptIndex.html')

# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_list(request):
    
    return render(request,'Customer/ReceiptList.html')

# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_receive(request):
    
    return render(request,'Customer/ReceiptReceive.html')


# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_send(request):
    
    return render(request,'Customer/ReceiptSend.html')

# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def credit_index(request):
    
    return render(request,'Customer/CreditIndex.html')


# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def credit_list(request):
    
    return render(request,'Customer/CreditList.html')


# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_confirm(request):
    
    return render(request,'Customer/receiptconfirm.html')


# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def prefroma(request):
    
    return render(request,'Customer/Prefroma.html')


# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customerfactor_sendassigndriver(request):
    
    return render(request,'Customer/CustomerFactorSendAssignDriver.html')

# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customerfactor_sendstatus(request):
    
    return render(request,'Customer/CustomerFactorSendStatus.html')

# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customerfactor_servicedoc(request):
    
    return render(request,'Customer/CustomerFactorServiceDoc.html')

# @cache_page(10)
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
            return redirect('customer:IndexInquiryResponse')

        else:
            
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
        return redirect('customer:IndexInquiry')
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

# @cache_page(10)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL', 'ROLE_ADMIN')
def prefactor(request):
    if request.method == 'POST':
        buyers = request.POST.getlist("buyer_id")
        obj_item_ids = request.POST.getlist("obj_item_id")
        amounts = request.POST.getlist("amount")

        # Check if the lengths of obj_item_ids and amounts match
        if len(obj_item_ids) != len(amounts):
            return HttpResponse("Invalid form data")

        for obj_item_id, amount in zip(obj_item_ids, amounts):
            post_data = {
                "buyer_id": buyers[0],  # Assuming buyer_id is the same for all rows
                "obj_item_id": obj_item_id,
                "amount": amount,
                "register": request.POST.get("register"),
                "reg_dt": datetime.datetime.now(),
            }

            form = NewPreFactor(post_data)
            if form.is_valid():
                form.save()
            else:
                return HttpResponse("Invalid form")

        return redirect("customer:customerindex")

    else:
        form = NewPreFactor()

    context = {
        'form': form,
    }
    return render(request, 'CustomerIndex.html', context)
    
    