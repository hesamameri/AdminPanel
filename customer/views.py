from datetime import timezone
import datetime
import json
from django.core import serializers
from django.http import HttpResponse
from django.urls import reverse
from .utilities import get_object_or_none
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import F
from django.utils import timezone
from customer.templatetags.converter_tags import subtract
from ticket.models import Ticket
from .models import Contract, ContractCity, CreditSumSVA, DepoInit, DepoSend, Factor, FactorAddress, FactorPayway, ObjItem, ObjItemCity, ObjItemSpec, ObjPayment, ObjSend, ObjSpec, PreFactor, ProductSVA, VendorBuyerSVA, VendorBuyerSubSVA
from .models import CustomerSubSVA, CustomerSva, FactorComment, FactorDocument, FactorItem, FactorSVA, ObjItemSVA, ShopCustomerCount
from django.core.paginator import Paginator, EmptyPage
from collections import defaultdict
from django.db.models import Case, When, Value, IntegerField
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
from .forms import NewFactorAddress, NewFactorItem, NewFactorPayway, NewInquiry, NewObjItem,NewObjItemSpec, NewObjPayment, NewPreFactor
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum, F, Value, CharField, Case, When,FloatField,Subquery, OuterRef
from django.db.models.functions import Coalesce
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
                
                print(pay_data)
                
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
    print("factor_id: ", factor_id) 
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
                 # New query to get the sended field from FactorItemBalanceSVA
                factor_item_balance_sva = FactorItemBalanceSVA.objects.filter(factor_id=factor_id).values('factor_item_id', 'sended')

                # Create a dictionary to map factor_item_id to sended value
                sended_dict = {item['factor_item_id']: item['sended'] for item in factor_item_balance_sva}

                # Attach the sended value to each factor_item
                for item in factor_item:
                    item.sended = sended_dict.get(item.factor_item_id)
                factor_item_ids = factor_item.values('factor_item_id')
                # print(factor_item_ids)
                factor_depo_data = DepoSend.objects.filter(source_id__in = factor_item_ids)
                # print(factor_depo_data)
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
                # ------------------------------------------------------------------
                # depo assign section
                # have to use the ObjItemCity model here to retrieve the correct
                depo_addresses = FactorAddress.objects.filter(factor_id=factor_id)
                cities = depo_addresses.values('city_id')
                depo_itemcity = ObjItemCity.objects.filter(city_id__in=cities)
                depo_fac = depo_itemcity.values('obj_item_id')
                depos = ObjItem.objects.filter(obj_item_id__in=depo_fac, obj_id=1352)
                factor_item_depo = factor_item.values_list('obj_item_id', flat=True)

                # Create a dictionary to store depo data
                depo_data_dict = {}

                # Iterate over each address
                for address in depo_addresses:
                    city_id = address.city_id
                    depo_itemcity = ObjItemCity.objects.filter(city_id=city_id)
                    depo_fac = depo_itemcity.values_list('obj_item_id', flat=True)
                    depos = ObjItem.objects.filter(obj_item_id__in=depo_fac, obj_id=1352)

                    # Create a list to store depo data for this address
                    depo_data = []

                    # Create a set to keep track of depo IDs that have already been processed
                    processed_depo_ids = set()

                    # Iterate over each depo
                    for depo in depos:
                        # Check if this depo has already been processed
                        if depo.obj_item_id not in processed_depo_ids:
                            # Iterate over each product in factor_item_depo
                            for good in factor_item_depo:
                                aggregated = (
                                    DepoInit.objects
                                    .filter(depo=depo.obj_item_id, obj_item=good)
                                    .aggregate(
                                        total_in_amount=Coalesce(Sum('in_amount'), Value(0)),
                                        total_out_amount=Coalesce(Sum('out_amount'), Value(0))
                                    )
                                )
                                net_amount = aggregated['total_in_amount'] - aggregated['total_out_amount']
                                depo_data.append({
                                    'obj_item_id': depo.obj_item_id,
                                    'title': depo.title,
                                    'net_amount': net_amount,
                                    'related_obj_item_id': good,  # Include the related obj_item_id
                                })
                            # Mark this depo as processed
                            processed_depo_ids.add(depo.obj_item_id)

                    # Store the depo data for this address in the dictionary
                    depo_data_dict[str(city_id)] = depo_data

                # Convert the dictionary to JSON
                depo_data_json = json.dumps(depo_data_dict)
                print(depo_data_json)
                #--------------------------------------------------------------------
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
                    #depo
                    'depo_addresses':depo_addresses,
                    'depo_itemcity':depo_itemcity,
                    'depos':depos,
                    'depo_data_json': depo_data_json,
                }  
               
                
                return render(request,'Customer/Factor.html',context=context)
            else:
                print(obj_buyer)
                objinstance = ObjItem.objects.get(obj_item_id = obj_buyer)
                print(objinstance)
                new_factor = Factor.objects.create(buyer = objinstance,register = request.user.user_id,reg_dt = datetime.datetime.now())
                return redirect('customer:FactorWithFactorID', factor_id=new_factor.factor_id)


@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factor_add_depo(request):
    
    return redirect('customer:customerindex')





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
def factor_add_document(request,factor_id):
    
    if request.method == 'POST' and request.FILES['uri']:
        uploaded_file = request.FILES['uri']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)
        factor = get_object_or_404(Factor,factor_id=factor_id)
        document_type = request.POST.get('document_type')
        description = request.POST.get('description')
        register = request.POST.get('register')
        level_type = request.POST.get('level_type')
        document = FactorDocument(
            factor = factor,
            level_type = level_type,
            document_type=document_type,
            uri=file_url,  # save the relative path to the TextField
            description=description,
            register=register,  # assuming your user model has an id field
            reg_dt=timezone.now()
        )
        document.save()

        return redirect(reverse('customer:FactorWithFactorID', args=[factor_id]))   # Assuming you have a document_detail view

    else:
        return redirect(reverse('customer:FactorWithFactorID', args=[factor_id])) 

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factor_add_address(request,factor_id):
    if request.method == 'POST':
        factor = get_object_or_404(Factor,factor_id=factor_id)
        address_data = {
            'factor' : factor,
            'city_id': request.POST['city_id'],
            'phone':request.POST['phone'],
            'mobile':request.POST['mobile'],
            'address':request.POST['address'],
            'receiver':request.POST['receiver'],
        }
        addressform = NewFactorAddress(address_data)
        if addressform.is_valid():
            addressform.save()
            return redirect(reverse('customer:FactorWithFactorID', args=[factor_id]))  # Adjust the redirect as per your needs
        else:
            return redirect(reverse('customer:FactorWithFactorID', args=[factor_id]))  # Adjust the redirect as per your needs


        
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
            item = get_object_or_404(FactorItem, pk=element)
            item.delete()
            return redirect(reverse('customer:FactorWithFactorID', args=[request.POST.get('factor')]))
        elif request.POST['form_type'] == 'document':
            doc = get_object_or_404(FactorDocument, pk=element)
            doc.delete()
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
    
    customer_obj_id = 10301
    factors = Factor.objects.filter(acc_confirmer=None)

    contract_ids = factors.values_list('contract', flat=True)
    contract_objs = Contract.objects.filter(contract_id__in=contract_ids)
    vendor_ids = contract_objs.values_list('vendor', flat=True)
    vendor_objs = ObjItem.objects.filter(obj_item_id__in=vendor_ids)
    vendor_details = ObjItemSpec.objects.filter(obj_item_id__in=vendor_objs, obj_spec_id=113).values('val', 'obj_item_id')

    # Create a dictionary to map contract_id to vendor data
    vendor_data_dict = {}
    for contract, vendor, detail in zip(contract_objs, vendor_objs, vendor_details):
        vendor_data_dict[contract.contract_id] = {
            'name': vendor.name,
            'detail_val': detail['val']
        }

    buyer_ids = factors.values_list('buyer_id', flat=True)
    buyer_names = ObjItem.objects.filter(obj_item_id__in=buyer_ids).values('obj_item_id', 'name')
    buyer_name_dict = {buyer['obj_item_id']: buyer['name'] for buyer in buyer_names}

    obj_item_specs = ObjItemSpec.objects.filter(obj_item_id__in=buyer_ids).select_related('obj_spec')
    spec_data = defaultdict(dict)
    for spec in obj_item_specs:
        spec_data[spec.obj_item_id][spec.obj_spec.name] = spec.val

    combined_data = [
        {
            'factor': factor,
            'buyer_name': buyer_name_dict.get(factor.buyer_id),
            'obj_item_specs': spec_data.get(factor.buyer_id, {}),
            'vendor_data': vendor_data_dict.get(factor.contract_id, {'name': None, 'detail_val': None})
        }
        for factor in factors
    ]

    context = {
        'combined_data': combined_data,
    }

    return render(request, 'Customer/CustomerConfirmAccountList.html', context=context)






@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_confirm_salelist(request):

    factor_items = FactorItemBalanceSVA.objects.filter(sended__lt=F('amount'))
    # Getting the related Factor objects
    factor_ids = factor_items.values_list('factor_id', flat=True)
    factors = Factor.objects.filter(factor_id__in=factor_ids).values('factor_id', 'acc_confirm_dt', 'contract_id')

    # Creating a dictionary to easily look up the acc_confirm_dt and contract_id by factor_id
    factor_dict = {factor['factor_id']: {'acc_confirm_dt': factor['acc_confirm_dt'], 'contract_id': factor['contract_id']} for factor in factors}

    # Getting the related Contract objects
    contract_ids = [factor['contract_id'] for factor in factors]
    contract_cities = ContractCity.objects.filter(contract_id__in=contract_ids).values('contract_id', 'obj_item_id')

    # Getting the related ObjItem objects
    obj_item_ids = contract_cities.values_list('obj_item_id', flat=True)
    obj_items = ObjItem.objects.filter(obj_item_id__in=obj_item_ids).values('obj_item_id', 'name')

    # Creating a dictionary to easily look up the name by obj_item_id
    obj_item_name_dict = {obj_item['obj_item_id']: obj_item['name'] for obj_item in obj_items}

    template_data = []
    for factor_item in factor_items:
        factor_data = factor_dict.get(factor_item.factor_id, {})
        contract_city = contract_cities.filter(contract_id=factor_data.get('contract_id')).first()
        city_name = None
        if contract_city:
            city_name = obj_item_name_dict.get(contract_city['obj_item_id'])
        template_data.append({
            'factor_item': factor_item,
            'acc_confirm_dt': factor_data.get('acc_confirm_dt'),
            'city_name': city_name,
        })
    # print(template_data)
    context = {
        'factor_items': template_data,
    }

    return render(request, 'Customer/CustomerConfirmSaleList.html', context=context)
    







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
    
    if request.method == 'POST':
        print(request.POST)
        obj_payment_id = request.POST['obj_payment_id']
        obj_payment = get_object_or_404(ObjPayment, pk = obj_payment_id)
        obj_payment.price = request.POST['price']
        obj_payment.confirmer = request.user.user_id
        obj_payment.confirm_desc = request.POST['confirm_desc']
        obj_payment.confirm_status = request.POST['confirm_status']
        obj_payment.confirm_dt = datetime.datetime.now()
        obj_payment.save()
        return render(request, 'Customer/CustomerPaymentConfirm.html', context=context)
       

    else:
        obj_payments = ObjPayment.objects.filter(
          confirmer = None  
        )

        
        context = {
            'obj_payments':obj_payments,
        }
        

        return render(request, 'Customer/CustomerPaymentConfirm.html', context=context)
    
    


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
    if request.method == 'POST':
        print(request.POST)
        obj_payment_id = request.POST['obj_payment_id']
        obj_payment = get_object_or_404(ObjPayment, pk = obj_payment_id)
        obj_payment.doc_register_id = request.user.user_id
        obj_payment.roc_register_desc = request.POST['roc_register_desc']
        obj_payment.doc_no = request.POST['doc_no']
        obj_payment.doc_register_dt = datetime.datetime.now()
        obj_payment.save()
        return render(request, 'Customer/CustomerPaymentConfirm.html', context=context)
       

    else:
        obj_payments = ObjPayment.objects.filter(
            Q(confirmer__isnull=False) & (Q(doc_register_id__isnull=True) | Q(doc_register_dt__isnull=True))
        )

        
        context = {
            'obj_payments':obj_payments,
        }
        

        return render(request, 'Customer/CustomerPaymentConfirms.html', context=context)
    

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
    
    