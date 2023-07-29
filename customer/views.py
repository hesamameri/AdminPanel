from django.shortcuts import redirect, render
from django.db.models import F
from .models import CustomerSubSVA, CustomerSva, FactorSVA, ObjItemSVA, ShopCustomerCount
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from Administrator.permissions import permission_required
from django.db.models import Max
from customer import models
from .models import CustomerSubSVA
from .forms import NewCustomerForm
from .models import  Inquiry  # Import your models
from django.contrib.sessions.models import Session
from django.views.decorators.cache import cache_page

@cache_page(60)
@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL', 'ROLE_ADMIN')
def customer_index(request):
    if request.method == 'POST':
        form = NewCustomerForm(request.POST)
        if form.is_valid():
            new_customer = form.save()
            return redirect('customer:customerindexAll')
    else:
        customers = CustomerSubSVA.objects.values(
        'obj_item_id', 'name', 'title', 'status', 'city_id', 'codemeli', 'mobile', 'phone', 'reagent', 'address'
        # Add other fields as needed
    ).distinct()

    # Set the number of records to display per page
    records_per_page = 15

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
    }

    return render(request, 'Customer/CustomerIndex.html', context=context)



@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_index_all(request):
    # Get distinct obj_item_ids with maximum values for each field
    distinct_records = CustomerSva.objects.all()
    
    shops = ShopCustomerCount.objects.values('name')
    # Set the number of records to display per page
    records_per_page = 15

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
        'shops':shops,

    }
    # for i in page:
    #     print(i)
    return render(request, 'Customer/CustomerIndexAll.html', context=context)
    # return render(request,'Customer/CustomerIndexAll.html',context=context)



@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factor(request):
    
    return render(request,'Customer/Factor.html')








@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factor_index(request):
    factor_sva_objects = FactorSVA.objects.all()

    
    context = {'factor_sva_objects': factor_sva_objects}

    print(factor_sva_objects.first().factor)
    return render(request,'Customer/FactorList.html',context=context)

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_confirm_accountlist(request):
    
    return render(request,'Customer/CustomerConfirmAccountList.html')

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_confirm_salelist(request):
    
    return render(request,'Customer/CustomerConfirmSaleList.html')



@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_factor_assessment(request):
    
    return render(request,'Customer/CustomerFactorAssessment.html')


@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factor_send_index(request):
    
    return render(request,'Customer/FactorSendIndex.html')


@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_payment_confirm(request):
    
    return render(request,'Customer/CustomerPaymentConfirm.html')



@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_index(request):
    
    return render(request,'Customer/ReceiptIndex.html')


@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_list(request):
    
    return render(request,'Customer/ReceiptList.html')

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_receive(request):
    
    return render(request,'Customer/ReceiptReceive.html')

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_send(request):
    
    return render(request,'Customer/ReceiptSend.html')


@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def credit_index(request):
    
    return render(request,'Customer/CreditIndex.html')


@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def credit_list(request):
    
    return render(request,'Customer/CreditList.html')

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_confirm(request):
    
    return render(request,'Customer/receiptconfirm.html')


@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def prefroma(request):
    
    return render(request,'Customer/Prefroma.html')

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customerfactor_sendassigndriver(request):
    
    return render(request,'Customer/CustomerFactorSendAssignDriver.html')

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customerfactor_sendstatus(request):
    
    return render(request,'Customer/CustomerFactorSendStatus.html')


@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customerfactor_servicedoc(request):
    
    return render(request,'Customer/CustomerFactorServiceDoc.html')

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def customer_payment_confirms(request):
    inquiries = Inquiry.objects.all()

    context = {
        'inquiries': inquiries,
    }
    return render(request,'Customer/CustomerPaymentConfirms.html',context=context)

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def index_inquiry_response(request):
    inquiries = Inquiry.objects.all()

    context = {
        'inquiries': inquiries,
    }

    print(inquiries)

    return render(request, 'Customer/IndexInquiryResponse.html', context=context)




@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def index_inquiry(request):
    inquiries = Inquiry.objects.all()

    context = {
        'inquiries': inquiries,
    }
    return render(request,'Customer/IndexInquiry.html',context=context)

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def new_customer(request):
    
    return render(request,'Customer/NewCustomer.html')

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factorsend_installerprint(request):
    
    return render(request,'Customer/FactorSendInstallerPrint.html')

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def factor_send_print(request):
    
    return render(request,'Customer/FactorSendPrint.html')

@login_required(login_url='Administrator:login_view')
@permission_required('ROLE_PERSONEL','ROLE_ADMIN')
def receipt_print(request):
    
    return render(request,'Customer/ReceiptPrint.html')