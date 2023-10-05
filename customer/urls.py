from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'customer'
urlpatterns = [
    ########################################################### Customers
    ### customer
    path('customers/', views.customer_index, name='customerindex'),     
    path('customers/customer_pay/', views.customer_pay, name='CustomerPay'),  
    path('customers/customer_pay/<int:factor_id>', views.customer_pay, name='CustomerFactorPay'), 
    path('newcustomer', views.new_customer, name='NewCustomer'),
    path('customers/all', views.customer_index_all, name='customerindexAll'), 
    path('customerconfaccountlt', views.customer_confirm_accountlist, name='CustomerConfirmAccountList'),
    path('customerconfirmsalelist', views.customer_confirm_salelist, name='CustomerConfirmSaleList'),
    path('customerfactorassessment', views.customer_factor_assessment, name='CustomerFactorAssessment'),
    path('customers/prefactor', views.prefactor, name='PreFactor'),
    path('customerpaymentconfirm', views.customer_payment_confirm, name='CustomerPaymentConfirm'),
    path('receiptindex', views.receipt_index, name='ReceiptIndex'),
    path('receiptlist', views.receipt_list, name='ReceiptList'),
    path('receiptreceive', views.receipt_receive, name='ReceiptReceive'),
    path('receiptsend', views.receipt_send, name='ReceiptSend'),
    path('creditindex', views.credit_index, name='CreditIndex'),
    path('creditlist', views.credit_list, name='CreditList'),
    path('receiptconfirm', views.receipt_confirm, name='ReceiptConfirm'),
    path('prefroma', views.prefroma, name='Prefroma'),
    path('customerfactorservicedoc', views.customerfactor_servicedoc, name='CustomerFactorServiceDoc'),
    path('customerpaymentconfirms', views.customer_payment_confirms, name='CustomerPaymentConfirms'),
    path('indexinquiryresponse', views.index_inquiry_response, name='IndexInquiryResponse'),     
    path('indexinquiry', views.index_inquiry, name='IndexInquiry'),                              
    path('newcustomer', views.new_customer, name='NewCustomer'),
    ##### Factor 
    path('newfactor', views.new_factor, name='NewFactor'),  
    path('factor/by_buyer/<int:obj_buyer>/', views.factor, name='FactorWithBuyerID'),
    path('factor/by_factor/<int:factor_id>/', views.factor, name='FactorWithFactorID'),
    path('delete_factor_element/<int:element>/', views.delete_factor_element, name='delete_payway'),
    path('delete_factor_element/<int:element>/', views.delete_factor_element, name='delete_goods'),
    path('delete_factor_element/<int:element>/', views.delete_factor_element, name='delete_document'),
    path('add_goods_factor/<int:factor_id>/', views.factor_add_goods, name='add_goods_factor'),
    path('add_address_factor/<int:factor_id>/', views.factor_add_address, name='add_address_factor'),
    path('add_document_factor/<int:factor_id>/', views.factor_add_document, name='add_document_factor'),
    path('add_depo_factor/', views.factor_add_depo, name='add_depo_factor'),
    path('factorlist', views.factor_index, name='FactorList'),    
              
    

######################################### Drive
    path('factorsendindex', views.factor_send_index, name='FactorSendIndex'),
    path('factorsendindex/<int:obj_send_id>', views.factor_send_index, name='FactorSendIndexSend'),
    path('fetch_objsendserials/', views.fetch_obj_send_serials, name='fetch_obj_send_serials'),
    path('factorsendprint/<int:obj_send_id>', views.factor_send_print, name='FactorSendPrint'),
    path('addcomments/', views.add_comment, name='addcomment'),
    path('fetch_comments/', views.fetch_comments, name='fetch_comments'),
    path('customerfactorsendassigndriver', views.customerfactor_sendassigndriver, name='CustomerFactorSendAssignDriver'),
    path('customerfactorsendstatus', views.customerfactor_sendstatus, name='CustomerFactorSendStatus'),


########################################### Install
    path('factorinstallindex', views.factor_install_index, name='FactorInstallIndex'),
    path('factorinstallindexchange/<int:obj_send_id>/', views.factor_install_index, name='FactorInstallIndexChange'),    
    path('factorinstallassign', views.factor_install_assigninstaller, name='FactorInstallAssignInstaller'),
    path('factorinstallstatus', views.factor_install_sendstatus, name='FactorInstallSendStatus'),
    path('factorsendinstallerprint/<int:obj_send_id>', views.factorsend_installerprint, name='FactorSendInstallerPrint'),  
    
#############################################

    path('factorsendprint', views.factor_send_print, name='FactorSendPrint'),
    path('receiptprint', views.receipt_print, name='ReceiptPrint'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)