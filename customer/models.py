from django.db import models
# from ticket.models import *
# from Administrator.models import *


class CustomerSubSVA(models.Model):
    obj_item_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20, null=True)
    reagent = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    idno = models.CharField(max_length=20, null=True)
    codemeli = models.CharField(max_length=20, null=True)
    province_id = models.IntegerField(null=True)
    city_id = models.IntegerField(null=True)
    seller_buyer_id = models.IntegerField(null=True)
    sex_id = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'customer_sub_sva'
class CustomerSva(models.Model):
    obj_item_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    mobile = models.CharField(max_length=255, null=True)
    reagent = models.CharField(max_length=255, null=True)
    province_id = models.CharField(max_length=255, null=True)
    city_id = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    idno = models.CharField(max_length=255, null=True)
    codemeli = models.CharField(max_length=255, null=True)
    seller_buyer_id = models.CharField(max_length=255, null=True)
    sex_id = models.CharField(max_length=255, null=True)
    sex_title = models.CharField(max_length=255, null=True)
    brand_id = models.IntegerField(null=True)
    brand_name = models.CharField(max_length=255, null=True)
    brand_phone = models.CharField(max_length=255, null=True)
    brand_slung = models.CharField(max_length=255, null=True)

    class Meta:
        managed = False  # Tells Django that this model is not managed by Django's ORM
        db_table = 'customer_sva'  # Specify the database view name

class ShopCustomerCount(models.Model):
    obj_item_id = models.IntegerField()
    name = models.CharField(max_length=255)
    count = models.IntegerField()

    class Meta:
        managed = False  # Tells Django that this model is not managed by Django's ORM
        db_table = 'shop_customer_count'  # Specify the database view name

        
class ObjItemSVA(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    obj_type_id = models.IntegerField()
    obj_id = models.IntegerField()
    obj_item_id = models.IntegerField()
    obj_type_name = models.CharField(max_length=255)
    obj_type_title = models.CharField(max_length=255)
    obj_name = models.CharField(max_length=255)
    obj_title = models.CharField(max_length=255)
    obj_item_name = models.CharField(max_length=255)
    obj_item_title = models.CharField(max_length=255)

    class Meta:
        managed = False  # Tells Django that this model is not managed by Django's ORM
        db_table = 'obj_item_sva'  # Specify the database view name

class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=4, blank=True, null=True, db_comment='نوع قرارداد یا خرید است و یا قرار فروش')
    vendor = models.ForeignKey('ObjItem', models.DO_NOTHING, db_column='vendor', blank=True, null=True, db_comment='Vendor buyers')
    contract_no = models.CharField(max_length=255, blank=True, null=True)
    start_dt = models.CharField(max_length=10, blank=True, null=True)
    end_dt = models.CharField(max_length=10, blank=True, null=True)
    prepaid_price = models.FloatField(blank=True, null=True)
    prepaid_doc_no = models.FloatField(blank=True, null=True)
    prepaider = models.IntegerField(blank=True, null=True)
    prepaid_dt = models.DateTimeField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    confirm_dt = models.DateTimeField(blank=True, null=True)
    confirmer = models.IntegerField(blank=True, null=True)
    signer = models.IntegerField(blank=True, null=True)
    sign_dt = models.DateTimeField(blank=True, null=True)
    sign_description = models.TextField(blank=True, null=True)
    stop_dt = models.DateTimeField(blank=True, null=True)
    stoper = models.IntegerField(blank=True, null=True)
    stop_description = models.TextField(blank=True, null=True)
    contract_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract'

class ContractCast(models.Model):
    contract_cast_id = models.AutoField(primary_key=True)
    contract_item = models.ForeignKey('ContractItem', models.DO_NOTHING, blank=True, null=True)
    start_dt = models.DateField(blank=True, null=True)
    end_dt = models.DateField(blank=True, null=True)
    law_paper = models.IntegerField(blank=True, null=True)
    cast_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_cast'

class ContractCity(models.Model):
    contract_city_id = models.AutoField(primary_key=True)
    contract = models.ForeignKey('Contract', models.DO_NOTHING, blank=True, null=True)
    obj_item_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_city'
    
class ContractDiscount(models.Model):
    contract_discount_id = models.AutoField(primary_key=True)
    contract = models.ForeignKey('Contract', models.DO_NOTHING, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    percent_price = models.IntegerField(blank=True, null=True)
    fixed_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_discount'
        db_table_comment = 'تخفیفاتی که به صورت بازه ای شامل حال فروشنده خواهد شد'


class ContractItem(models.Model):
    contract_item_id = models.AutoField(primary_key=True)
    contract = models.ForeignKey('Contract', models.DO_NOTHING, blank=True, null=True)
    obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    unit_price = models.FloatField(blank=True, null=True)
    wage = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_item'
        db_table_comment = 'چه چیزی با چه نسخه ای (درصورت نیاز) با چه مشخصات مبلغی که در قرارداد ذکر شده است قرار است\nخریدش انجام شود و یا ارسالش انجام شود'


class ContractItemBom(models.Model):
    contract_item_bom_id = models.AutoField(primary_key=True)
    contract_item = models.ForeignKey('ContractItem', models.DO_NOTHING, blank=True, null=True)
    obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    drop_amount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_item_bom'


class ContractItemOrgan(models.Model):
    contract_item_organ_id = models.AutoField(primary_key=True)
    contract_item = models.ForeignKey('ContractItem', models.DO_NOTHING, blank=True, null=True)
    obj_item_id = models.IntegerField(blank=True, null=True)
    percent_amount = models.IntegerField(blank=True, null=True)
    fixed_amount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_item_organ'


class ContractItemTiming(models.Model):
    contract_item_timing_id = models.AutoField(primary_key=True)
    contract_item = models.ForeignKey('ContractItem', models.DO_NOTHING, blank=True, null=True)
    depo = models.ForeignKey('ObjItem', models.DO_NOTHING)
    amount = models.FloatField(blank=True, null=True)
    start_dt = models.DateTimeField(blank=True, null=True)
    end_dt = models.DateTimeField(blank=True, null=True)
    stop_dt = models.DateTimeField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField()
    stop_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_item_timing'

class DepoConfilict(models.Model):
    depo_confilict_id = models.AutoField(primary_key=True)
    depo_id = models.IntegerField()
    goods = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    register = models.IntegerField()
    reg_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'depo_confilict'
    
class DepoInit(models.Model):
    depo_init_id = models.AutoField(primary_key=True)
    depo = models.ForeignKey('ObjItem', models.DO_NOTHING, blank=True, null=True)
    obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING, related_name='depoinit_obj_item_set', blank=True, null=True)
    init_type = models.CharField(max_length=13)
    in_amount = models.IntegerField(blank=True, null=True)
    out_amount = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    unit_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'depo_init'

class DepoSend(models.Model):
    depo_send_id = models.AutoField(primary_key=True)
    source_type = models.CharField(max_length=6, blank=True, null=True, db_comment='FACTORE')
    source_id = models.IntegerField(blank=True, null=True, db_comment='factor_item_id,')
    goods = models.IntegerField(blank=True, null=True)
    depo_id = models.IntegerField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    send_status = models.CharField(max_length=7, blank=True, null=True)
    send_desc = models.TextField(blank=True, null=True)
    receiver = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'depo_send'


class DepoToDepo(models.Model):
    depo_to_depo_id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    confirmer = models.IntegerField(blank=True, null=True)
    confirm_dt = models.DateTimeField(blank=True, null=True)
    sender_id = models.IntegerField(blank=True, null=True)
    sender_dt = models.DateTimeField(blank=True, null=True)
    sender_desc = models.TextField(blank=True, null=True)
    receiver_id = models.IntegerField(blank=True, null=True)
    receiver_dt = models.DateTimeField(blank=True, null=True)
    receiver_desc = models.TextField(blank=True, null=True)
    canceler = models.IntegerField(blank=True, null=True)
    cancel_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'depo_to_depo'

class DepoToDepoItem(models.Model):
    depo_to_depo = models.ForeignKey('DepoToDepo', models.DO_NOTHING)
    obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING, blank=True, null=True)
    amount_src = models.FloatField()
    amount_dst = models.FloatField(blank=True, null=True)
    reg_src = models.IntegerField()
    reg_src_dt = models.DateTimeField()
    reg_dst = models.IntegerField(blank=True, null=True)
    reg_dst_dt = models.DateTimeField(blank=True, null=True)
    depo_src = models.IntegerField()
    depo_dst = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'depo_to_depo_item'


class DocItem(models.Model):
    doc_item_id = models.AutoField(primary_key=True)
    doc_id = models.IntegerField()
    kol = models.IntegerField()
    moeen = models.IntegerField()
    tafsily = models.IntegerField()
    joz1 = models.IntegerField()
    joz2 = models.IntegerField()
    joz3 = models.IntegerField()
    joz4 = models.IntegerField()
    description = models.IntegerField()
    debit = models.IntegerField()
    credit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'doc_item'
class Factor(models.Model):
    factor_id = models.AutoField(primary_key=True)
    contract = models.ForeignKey('Contract', models.DO_NOTHING, blank=True, null=True)
    buyer = models.ForeignKey('ObjItem', models.DO_NOTHING)
    factore_desc = models.TextField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    reg_status = models.CharField(max_length=7, blank=True, null=True)
    seller_factor_id = models.BigIntegerField(blank=True, null=True, db_comment='شماره فاکتور مشتری است\nکه تابع زیر عدد فوق را بر اساس کد فروشنده تولید خواهد کرد\ngetNextCustomSeq')
    confirmer = models.IntegerField(blank=True, null=True)
    confirm_dt = models.DateTimeField(blank=True, null=True)
    depo_id = models.IntegerField(blank=True, null=True)
    sale_confirmer = models.IntegerField(blank=True, null=True)
    sale_confirm_dt = models.DateTimeField(blank=True, null=True)
    acc_confirmer = models.IntegerField(blank=True, null=True)
    acc_confirm_dt = models.DateTimeField(blank=True, null=True)
    acc_status = models.IntegerField(blank=True, null=True)
    acc_description = models.CharField(max_length=255, blank=True, null=True)
    receipt_doc_printer_id = models.PositiveIntegerField(blank=True, null=True)
    receipt_doc_print_dt = models.DateTimeField(blank=True, null=True)
    sale_confirm_status = models.IntegerField(blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True, db_comment='شهر تحویل گیرنده فاکتور فوق\nدرصورتی که خریداری بار را برای آدرس دیگری خریداری کرده باشد')
    address = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    receiver = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factor'

class FactorSVA(models.Model):
    contract_id = models.IntegerField(primary_key=True)
    vendor = models.IntegerField()
    vendor_name = models.CharField(max_length=255)
    contract_no = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    province_name = models.CharField(max_length=100)
    city_name = models.CharField(max_length=100)
    factor = models.ForeignKey(Factor, on_delete=models.DO_NOTHING, related_name='factor_sva_set')
    buyer_id = models.IntegerField()
    buyer_name = models.CharField(max_length=255)
    reg_dt = models.DateTimeField()
    acc_confirm_dt = models.DateTimeField()
    acc_description = models.TextField()
    sale_confirm_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'factor_sva'
class FactorAddress(models.Model):
    factor_address_id = models.AutoField(primary_key=True)
    factor = models.ForeignKey('Factor', models.DO_NOTHING, blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    receiver = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factor_address'


class FactorComment(models.Model):
    factor_comment_id = models.AutoField(primary_key=True)
    factor_id = models.IntegerField()
    level = models.CharField(max_length=7)
    body = models.TextField()
    register = models.IntegerField()
    reg_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'factor_comment'


class FactorDocument(models.Model):
    factor_document_id = models.AutoField(primary_key=True)
    factor = models.ForeignKey('Factor', models.DO_NOTHING)
    level_type = models.CharField(max_length=7)
    document_type = models.CharField(max_length=8)
    uri = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    hash = models.CharField(max_length=256, blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'factor_document'


class FactorItem(models.Model):
    factor_item_id = models.AutoField(primary_key=True)
    factor = models.ForeignKey('Factor', models.DO_NOTHING)
    obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING)
    amount = models.FloatField()
    unit_price = models.FloatField()
    price = models.FloatField(blank=True, null=True)
    discount_percent = models.FloatField(blank=True, null=True)
    discount_price = models.FloatField()
    related_factor_item_id = models.IntegerField(blank=True, null=True)
    register = models.IntegerField()
    reg_dt = models.DateTimeField(blank=True, null=True)
    document_delivery_id = models.IntegerField(blank=True, null=True)
    document_delivery_dt = models.DateTimeField(blank=True, null=True)
    document_recieve_id = models.IntegerField(blank=True, null=True)
    document_recieve_dt = models.DateTimeField(blank=True, null=True)
    depo_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factor_item'


class FactorItemOrgan(models.Model):
    factor_item_organ_id = models.AutoField(primary_key=True)
    factor_item = models.ForeignKey('FactorItem', models.DO_NOTHING)
    organ = models.ForeignKey('ObjItem', models.DO_NOTHING)
    percent_rate = models.FloatField(blank=True, null=True)
    fixed_rate = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factor_item_organ'


class FactorPayway(models.Model):
    factor_payway_id = models.AutoField(primary_key=True)
    factor = models.ForeignKey('Factor', models.DO_NOTHING)
    pay_level = models.CharField(max_length=7)
    pay_type = models.CharField(max_length=9)
    price = models.FloatField()
    bank = models.ForeignKey('ObjItem', models.DO_NOTHING, blank=True, null=True)
    cheque_owner = models.CharField(max_length=255, blank=True, null=True)
    no = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField()
    receipe_id = models.IntegerField(blank=True, null=True)
    receip_dt = models.DateTimeField(blank=True, null=True)
    receive_doc_id = models.IntegerField(blank=True, null=True, db_comment='چه کسی از شرکت چک را تحویل گرفته است')
    receieve_doc_dt = models.DateTimeField(blank=True, null=True, db_comment='در چه تاریخی چک را تایید تحویل مامور شده')
    receieve_doc_description = models.TextField(blank=True, null=True)
    receive_acc_id = models.IntegerField(blank=True, null=True, db_comment='چه کسی در واحد مالی دریافت چک را تایید کرده است')
    receive_acc_dt = models.DateTimeField(blank=True, null=True, db_comment='در چه تاریخی واحد مالی دریافت چک را تایید کرده است')
    receive_acc_description = models.TextField(blank=True, null=True)
    receive_doc_no = models.CharField(max_length=255, blank=True, null=True, db_comment='شماره سندی چک ثبت سیستم شده است')

    class Meta:
        managed = False
        db_table = 'factor_payway'
class Inquiry(models.Model):
    inquiry_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey('ObjItem', models.DO_NOTHING, blank=True, null=True)
    first_control = models.IntegerField()
    bank = models.ForeignKey('ObjItem', models.DO_NOTHING, related_name='inquiry_bank_set', blank=True, null=True)
    bank_branch = models.CharField(max_length=255, blank=True, null=True)
    bank_code = models.CharField(max_length=255, blank=True, null=True)
    account_owner = models.CharField(max_length=255, blank=True, null=True)
    account_owner_nat_code = models.CharField(max_length=255, blank=True, null=True)
    account_no = models.CharField(max_length=255, blank=True, null=True)
    account_sayadi = models.CharField(max_length=255, blank=True, null=True)
    account_shaba = models.CharField(max_length=255, blank=True, null=True)
    cheque_image = models.TextField(blank=True, null=True)
    cheque_price = models.FloatField(blank=True, null=True)
    cheque_count = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    sms_inquiry = models.IntegerField(blank=True, null=True)
    indirect_inquiry = models.IntegerField(blank=True, null=True)
    confirm_desc = models.CharField(max_length=255, blank=True, null=True)
    confirmer = models.IntegerField(blank=True, null=True)
    confirm_dt = models.DateTimeField(blank=True, null=True)
    confirm_status = models.CharField(max_length=12, blank=True, null=True)
    shower = models.IntegerField(blank=True, null=True)
    show_dt = models.DateTimeField(blank=True, null=True)
    action = models.CharField(max_length=6, blank=True, null=True, db_comment='در مرحله آخر تصمیم گرفته میشود نصب به استعلام فوق فاکتور صادر شود و یا نشود\nو آیتم فوق نشان میدهد که \nshower\nفوق چه تصمیمی گرفته است')
    actioner = models.IntegerField(blank=True, null=True)
    action_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inquiry'

class Obj(models.Model):
    obj_id = models.AutoField(primary_key=True)
    obj_type = models.ForeignKey('ObjType', models.DO_NOTHING)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obj'


# class ObjDocument(models.Model):
#     obj_document_id = models.AutoField(primary_key=True)
#     source_type = models.CharField(max_length=255)
#     source_id = models.IntegerField()
#     document_type = models.CharField(max_length=255)
#     uri = models.CharField(max_length=255)
#     description = models.TextField()
#     hash = models.CharField(max_length=255)

#     class Meta:
#         managed = False
#         db_table = 'obj_document'


class ObjItem(models.Model):
    obj_item_id = models.AutoField(primary_key=True)
    obj = models.ForeignKey(Obj, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obj_item'


# class ObjItemCity(models.Model):
#     obj_item_city_id = models.AutoField(primary_key=True)
#     obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING)
#     city = models.ForeignKey('ObjItem', models.DO_NOTHING, related_name='objitemcity_city_set')

#     class Meta:
#         managed = False
#         db_table = 'obj_item_city'
#         db_table_comment = 'هدف از طراحی جدول فوق برای انبارها بوده است\nکه هر انبار به شهرهایی سرویس میدهد و انباردار مربوطه فقط فاکتروهای منطقه خودش را مشاهده کند\nهمپوشانی انبار و منطقه اگر وجود داشته باشد امکان ارسال دوباره کالا خواهد شد'


# class ObjItemConfirmer(models.Model):
#     obj_item_confirmer_id = models.AutoField(primary_key=True)
#     obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING)
#     register_chart = models.ForeignKey(Chart, models.DO_NOTHING, blank=True, null=True, db_comment='انبار جارت دریافت کننده\nلوازم مصرفی ثبت کننده و اگر خالی بود همه میتوانند ثبت کنند')
#     confirmer_chart = models.ForeignKey(Chart, models.DO_NOTHING, related_name='objitemconfirmer_confirmer_chart_set', blank=True, null=True)
#     counter_chart = models.ForeignKey(Chart, models.DO_NOTHING, related_name='objitemconfirmer_counter_chart_set', blank=True, null=True, db_comment='انبار چارت شمارش کننده\nلوازم مصرفی تصویب کننده است و اگر خالی بود تصویب کننده همان تایید کننده می باشد')
#     register_hierarchical = models.IntegerField(blank=True, null=True, db_comment='آیا زیر دست های چارت فوق میتوانند ثبت کننده باشند')
#     confirmer_hierarchical = models.IntegerField()
#     depo_id = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'obj_item_confirmer'
#         db_table_comment = 'انبارها\nثثبت کننده\nتایید کننده کیفیت\nشمارش کننده انبار\n\nلوازم مصرفی\nچه کسی صدور میزند اگر خالی بود همه میتوانند صدور بزنند\nچه کسی میتواند این کالا را تایید کند که خریداری شود و نمیتواند خالی باشد\nتصویب کننده اگر تصویب کننده کالا داشت باید تصویب شود وگرنه تایید کننده تصویب کننده هم خواهد بود'

class ObjSpec(models.Model):
    obj_spec_id = models.AutoField(primary_key=True)
    obj = models.ForeignKey(Obj, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    data_type = models.CharField(max_length=100, blank=True, null=True)
    default_value = models.TextField(blank=True, null=True)
    requirement = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    min_len = models.IntegerField(blank=True, null=True)
    max_len = models.IntegerField(blank=True, null=True)
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)
    pattern = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obj_spec'
class ObjItemSpec(models.Model):
    obj_item_spec_id = models.AutoField(primary_key=True)
    obj_item = models.ForeignKey(ObjItem, models.DO_NOTHING, blank=True, null=True)
    obj_spec = models.ForeignKey(ObjSpec, models.DO_NOTHING, blank=True, null=True)
    val = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obj_item_spec'

class ObjPayment(models.Model):
    obj_payment_id = models.AutoField(primary_key=True)
    obj_item_id = models.IntegerField()
    type = models.CharField(max_length=9)
    source_type = models.CharField(max_length=255)
    source_id = models.IntegerField()
    bank_id = models.IntegerField(blank=True, null=True)
    no = models.CharField(max_length=255, blank=True, null=True)
    branch_code = models.CharField(max_length=255, blank=True, null=True)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)
    register = models.IntegerField()
    reg_dt = models.DateTimeField()
    confirmer = models.IntegerField(blank=True, null=True)
    confirm_dt = models.DateTimeField(blank=True, null=True)
    confirm_status = models.CharField(max_length=7, blank=True, null=True)
    confirm_desc = models.CharField(max_length=255, blank=True, null=True)
    receip_id = models.IntegerField(blank=True, null=True)
    receip_dt = models.DateTimeField(blank=True, null=True)
    receive_doc_id = models.IntegerField(blank=True, null=True)
    receive_doc_dt = models.DateTimeField(blank=True, null=True)
    receive_doc_description = models.TextField(blank=True, null=True)
    receive_acc_id = models.IntegerField(blank=True, null=True)
    receive_acc_dt = models.DateTimeField(blank=True, null=True)
    receive_acc_desc = models.TextField(blank=True, null=True)
    doc_register_id = models.IntegerField(blank=True, null=True)
    doc_register_dt = models.DateTimeField(blank=True, null=True)
    doc_no = models.IntegerField(blank=True, null=True)
    roc_register_desc = models.TextField(blank=True, null=True)

    class Meta:
         managed = False
         db_table = 'obj_payment'


class ObjSend(models.Model):
    obj_send_id = models.AutoField(primary_key=True)
    action = models.CharField(max_length=7)
    source_type = models.CharField(max_length=6, blank=True, null=True)
    source_id = models.IntegerField()
    print_id = models.IntegerField(blank=True, null=True)
    print_dt = models.DateTimeField(blank=True, null=True)
    print_desc = models.CharField(max_length=255, blank=True, null=True)
    drive_id = models.IntegerField(blank=True, null=True)
    doer2_id = models.IntegerField(blank=True, null=True)
    doer1_id = models.IntegerField(blank=True, null=True)
    drive_dt = models.DateTimeField(blank=True, null=True)
    drive_desc = models.CharField(max_length=255, blank=True, null=True)
    drive_status = models.CharField(max_length=7, blank=True, null=True)
    drive_status_id = models.IntegerField(blank=True, null=True)
    drive_status_dt = models.DateTimeField(blank=True, null=True)
    drive_status_desc = models.CharField(max_length=255, blank=True, null=True)
    drive_register = models.IntegerField(blank=True, null=True)
    assesmenter = models.IntegerField(blank=True, null=True)
    assesment_dt = models.DateTimeField(blank=True, null=True)
    assesment_desc = models.TextField(blank=True, null=True)
    assesment_opinion = models.IntegerField(blank=True, null=True)
    docer = models.IntegerField(blank=True, null=True)
    doc_dt = models.DateTimeField(blank=True, null=True)
    doc_desc = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    assesmenter_shop = models.IntegerField(blank=True, null=True)
    assesmenter_shop_dt = models.DateTimeField(blank=True, null=True)
    assesment_seller = models.IntegerField(blank=True, null=True)
    assesment_shopper_desc = models.TextField(blank=True, null=True)
    assesment_shop = models.IntegerField(blank=True, null=True)
    assesment_drive_time = models.IntegerField(blank=True, null=True)
    assesmenter_service = models.IntegerField(blank=True, null=True)
    assesmenter_service_dt = models.DateTimeField(blank=True, null=True)
    assesment_servic_action = models.IntegerField(blank=True, null=True)
    assesment_service_dress = models.IntegerField(blank=True, null=True)
    assesment_service_status = models.IntegerField(blank=True, null=True)
    shop_desc = models.TextField(blank=True, null=True)
    isntall_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obj_send'


class ObjSendSerial(models.Model):
    obj_send_serial_id = models.AutoField(primary_key=True)
    obj_send_id = models.IntegerField(blank=True, null=True)
    factor_id = models.IntegerField()
    product_id = models.IntegerField()
    serial_drive = models.CharField(max_length=255, blank=True, null=True)
    serial = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obj_send_serial'





class ObjType(models.Model):
    obj_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    has_bom = models.IntegerField(blank=True, null=True)
    child_length = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obj_type'


class ObjTypeSpec(models.Model):
    obj_type_spec_id = models.AutoField(primary_key=True)
    obj_type = models.ForeignKey('ObjType', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    data_type = models.CharField(max_length=100, blank=True, null=True)
    default_value = models.TextField(blank=True, null=True)
    requirement = models.IntegerField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)
    min_len = models.IntegerField(blank=True, null=True)
    max_len = models.IntegerField(blank=True, null=True)
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)
    pattern = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obj_type_spec'

class PreFactor(models.Model):
    pre_factor_id = models.AutoField(primary_key=True)
    buyer_id = models.IntegerField(blank=True, null=True)
    obj_item_id = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    unit_price = models.IntegerField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pre_factor'
class ProductAdditional(models.Model):
    product_additional_id = models.AutoField(primary_key=True)
    obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING)
    amount = models.IntegerField(blank=True, null=True, db_comment='تعدادی که از کالای فوق باید به صورت خودکار به فاکتور افزوده شود')
    unit_price_rate = models.FloatField(blank=True, null=True)
    obj_item_add = models.ForeignKey(ObjItem, models.DO_NOTHING, related_name='productadditional_obj_item_add_set')
    unit_price_fixed = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_additional'
        db_table_comment = 'کالاهایی می باشد که به صورت خودکار به فاکتور افزوده خواهند شد\nیعنی با افزودن کالا به فاکتور به صورت خودذکار کالاهای فوق نیز به فاکتور افزوده خواهند شد'
class ProductDiscount(models.Model):
    product_discount_id = models.AutoField(primary_key=True)
    obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING)
    percent_rate = models.FloatField(blank=True, null=True)
    fixed_rate = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True, db_comment='تا تعداد فوق درصد تخفیفی که داده میشود')
    discount_type = models.CharField(max_length=4, blank=True, null=True)
    fixed_amount = models.IntegerField(blank=True, null=True, db_comment='در صورت رسیدن به تعداد مورد نظر به تعداد کالا با ضریب مشخص شده مبلغ افزوده شود')

    class Meta:
        managed = False
        db_table = 'product_discount'
        db_table_comment = 'تخفیفاتی که برای محصول در نظر گرفته شده است'



class Production(models.Model):
    production_id = models.IntegerField(primary_key=True)
    dt = models.DateTimeField()
    pdt = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    reg_dt = models.DateTimeField()
    register = models.IntegerField()
    confimer_dt = models.DateTimeField(blank=True, null=True)
    confirmer = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'production'