from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'customer'
urlpatterns = [
    path('customers/', views.customer_index, name='customerindex'),
    path('customers/all', views.customer_index_all, name='customerindexAll'),
    path('factor', views.factor, name='Factor'),
    path('factorlist', views.factor_index, name='FactorList'),
    path('customerconfaccountlt', views.customer_confirm_accountlist, name='CustomerConfirmAccountList'),
    path('customerconfirmsalelist', views.customer_confirm_salelist, name='CustomerConfirmSaleList'),
    path('customerfactorassessment', views.customer_factor_assessment, name='CustomerFactorAssessment'),
    path('factorsendindex', views.factor_send_index, name='FactorSendIndex'),
    path('customerpaymentconfirm', views.customer_payment_confirm, name='CustomerPaymentConfirm'),
    path('receiptindex', views.receipt_index, name='ReceiptIndex'),
    path('receiptlist', views.receipt_list, name='ReceiptList'),
    path('receiptreceive', views.receipt_receive, name='ReceiptReceive'),
    path('receiptsend', views.receipt_send, name='ReceiptSend'),
    path('creditindex', views.credit_index, name='CreditIndex'),
    path('creditlist', views.credit_list, name='CreditList'),
    path('receiptconfirm', views.receipt_confirm, name='ReceiptConfirm'),
    path('prefroma', views.prefroma, name='Prefroma'),
    path('customerfactorsendassigndriver', views.customerfactor_sendassigndriver, name='CustomerFactorSendAssignDriver'),
    path('customerfactorsendstatus', views.customerfactor_sendstatus, name='CustomerFactorSendStatus'),
    path('customerfactorservicedoc', views.customerfactor_servicedoc, name='CustomerFactorServiceDoc'),
    path('customerpaymentconfirms', views.customer_payment_confirms, name='CustomerPaymentConfirms'),
    path('indexinquiryresponse', views.index_inquiry_response, name='IndexInquiryResponse'),
    path('indexinquiry', views.index_inquiry, name='IndexInquiry'),
    path('newcustomer', views.new_customer, name='NewCustomer'),
    path('factorsendinstallerprint', views.factorsend_installerprint, name='FactorSendInstallerPrint'),
    path('factorsendprint', views.factor_send_print, name='FactorSendPrint'),
    path('receiptprint', views.receipt_print, name='ReceiptPrint'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)