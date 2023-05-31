# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Day(models.Model):
    dt = models.CharField(primary_key=True, max_length=10)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()

    class Meta:
        managed = False
        db_table = '_day'


class Sequence(models.Model):
    seq_id = models.AutoField(primary_key=True)
    seq_name = models.CharField(max_length=50)
    seq_group = models.CharField(max_length=10)
    seq_val = models.PositiveBigIntegerField()

    class Meta:
        managed = False
        db_table = '_sequence'


class TmpEmpFunction(models.Model):
    emp_function_id = models.IntegerField()
    person = models.IntegerField(blank=True, null=True)
    dt = models.CharField(max_length=10, db_collation='utf8_general_ci', blank=True, null=True)
    mdt = models.DateField(blank=True, null=True)
    shift_id = models.IntegerField(blank=True, null=True)
    function_kind_id = models.IntegerField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = '_tmp_emp_function'


class Bom(models.Model):
    bom_id = models.AutoField(primary_key=True)
    bom_ver = models.ForeignKey('BomVer', models.DO_NOTHING, blank=True, null=True)
    obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    drop_amount = models.FloatField(blank=True, null=True)
    tree_number = models.IntegerField(blank=True, null=True)
    tree_order = models.IntegerField(blank=True, null=True, db_comment='شماره درخت')
    tree_connect = models.CharField(max_length=255, blank=True, null=True, db_comment='در شاخه درخت فوق چه ورودی از چه درخت های دیگری وجود دارد\nان درخت ها قبلا نباید به درخت دیگری افزوده باشند')
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bom'


class BomEqual(models.Model):
    bom_equal_id = models.AutoField(primary_key=True)
    bom = models.ForeignKey(Bom, models.DO_NOTHING, blank=True, null=True)
    obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    equal_group = models.CharField(max_length=255, blank=True, null=True, db_comment='اگر چند قطعه با هم تشکیل گروه مصرفی معادل را بدهند با آیتم فوق گروهشان مشخص میشود')

    class Meta:
        managed = False
        db_table = 'bom_equal'


class BomVer(models.Model):
    bom_ver_id = models.AutoField(primary_key=True)
    obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING, blank=True, null=True)
    version = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True, db_comment='به نام محصول اضافه میشود و برای ایجاد تفکیک که به چه روشی تولید شده است\nدر این گونه محصولات قیمت محصول نهایی تفاوتی با هم نمیکنند')
    amount = models.IntegerField(db_comment='برای تولید تعداد فوق چه تعداد مواد نباز می باشد')
    status = models.IntegerField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    main_version = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bom_ver'


class Calendar(models.Model):
    calendar_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calendar'


class CalendarHoliday(models.Model):
    calendar_holiday_id = models.AutoField(primary_key=True)
    calendar = models.ForeignKey(Calendar, models.DO_NOTHING, blank=True, null=True)
    dt = models.CharField(max_length=10, blank=True, null=True)
    mdt = models.DateField(blank=True, null=True)
    rec_type = models.CharField(max_length=1, blank=True, null=True, db_comment='نوع تعطیلات\n  و سایر رسمی، مناسبتی')
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calendar_holiday'


class Chart(models.Model):
    chart_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chart'


class ChartCity(models.Model):
    chart_city_id = models.AutoField(primary_key=True)
    chart_id = models.IntegerField(blank=True, null=True)
    city_type = models.CharField(max_length=6, blank=True, null=True)
    city_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'chart_city'


class ChartRole(models.Model):
    chart_role_id = models.AutoField(primary_key=True)
    field_role = models.ForeignKey('Role', models.DO_NOTHING, db_column='_role', to_field='name', blank=True, null=True)  # Field renamed because it started with '_'.
    chart = models.ForeignKey(Chart, models.DO_NOTHING, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chart_role'


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
    contract = models.ForeignKey(Contract, models.DO_NOTHING, blank=True, null=True)
    obj_item_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_city'


class ContractDiscount(models.Model):
    contract_discount_id = models.AutoField(primary_key=True)
    contract = models.ForeignKey(Contract, models.DO_NOTHING, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    percent_price = models.IntegerField(blank=True, null=True)
    fixed_price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_discount'
        db_table_comment = 'تخفیفاتی که به صورت بازه ای شامل حال فروشنده خواهد شد'


class ContractItem(models.Model):
    contract_item_id = models.AutoField(primary_key=True)
    contract = models.ForeignKey(Contract, models.DO_NOTHING, blank=True, null=True)
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
    contract_item = models.ForeignKey(ContractItem, models.DO_NOTHING, blank=True, null=True)
    obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    drop_amount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_item_bom'


class ContractItemOrgan(models.Model):
    contract_item_organ_id = models.AutoField(primary_key=True)
    contract_item = models.ForeignKey(ContractItem, models.DO_NOTHING, blank=True, null=True)
    obj_item_id = models.IntegerField(blank=True, null=True)
    percent_amount = models.IntegerField(blank=True, null=True)
    fixed_amount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contract_item_organ'


class ContractItemTiming(models.Model):
    contract_item_timing_id = models.AutoField(primary_key=True)
    contract_item = models.ForeignKey(ContractItem, models.DO_NOTHING, blank=True, null=True)
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


class DayOfWeek(models.Model):
    dow_first = models.IntegerField(blank=True, null=True)
    dow_dt = models.IntegerField(blank=True, null=True)
    mdt = models.DateTimeField(blank=True, null=True)
    dt = models.CharField(max_length=100, blank=True, null=True)
    week = models.FloatField(blank=True, null=True)
    field_rownum_rownum_1 = models.FloatField(db_column='@rownum := @rownum + 1', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'day_of_week'


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
    depo_to_depo = models.ForeignKey(DepoToDepo, models.DO_NOTHING)
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


class EmpFunction(models.Model):
    emp_function_id = models.AutoField(primary_key=True)
    person = models.IntegerField(blank=True, null=True)
    dt = models.CharField(max_length=10, blank=True, null=True)
    mdt = models.DateField(blank=True, null=True)
    shift_id = models.IntegerField(blank=True, null=True)
    function_kind = models.ForeignKey('FunctionKind', models.DO_NOTHING, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emp_function'


class EmpOvertime(models.Model):
    emp_overtime_id = models.AutoField(primary_key=True)
    rec_type = models.CharField(max_length=8)
    person = models.IntegerField()
    start_dt = models.CharField(max_length=10)
    end_dt = models.CharField(max_length=10, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField()
    confirmer = models.IntegerField(blank=True, null=True)
    confirm_dt = models.DateTimeField(blank=True, null=True)
    confirm_status = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emp_overtime'
        db_table_comment = 'درخواست مرخصی، اضافه کار، ماموریت'


class EmpTrans(models.Model):
    emp_trans_id = models.BigAutoField(primary_key=True)
    person = models.IntegerField(blank=True, null=True)
    device = models.IntegerField(blank=True, null=True, db_comment='شماره دستگاه کارتخوان و یادستی وارد شده است')
    dttime = models.DateTimeField(blank=True, null=True)
    dt = models.CharField(max_length=10, blank=True, null=True)
    trans_time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=7)

    class Meta:
        managed = False
        db_table = 'emp_trans'
        unique_together = (('person', 'dttime'),)


class Factor(models.Model):
    factor_id = models.AutoField(primary_key=True)
    contract = models.ForeignKey(Contract, models.DO_NOTHING, blank=True, null=True)
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


class FactorAddress(models.Model):
    factor_address_id = models.AutoField(primary_key=True)
    factor = models.ForeignKey(Factor, models.DO_NOTHING, blank=True, null=True)
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
    factor = models.ForeignKey(Factor, models.DO_NOTHING)
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
    factor = models.ForeignKey(Factor, models.DO_NOTHING)
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
    factor_item = models.ForeignKey(FactorItem, models.DO_NOTHING)
    organ = models.ForeignKey('ObjItem', models.DO_NOTHING)
    percent_rate = models.FloatField(blank=True, null=True)
    fixed_rate = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factor_item_organ'


class FactorPayway(models.Model):
    factor_payway_id = models.AutoField(primary_key=True)
    factor = models.ForeignKey(Factor, models.DO_NOTHING)
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


class Form(models.Model):
    form_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'form'


class FormRole(models.Model):
    form_role_id = models.AutoField(primary_key=True)
    form = models.ForeignKey(Form, models.DO_NOTHING, blank=True, null=True)
    field_role = models.ForeignKey('Role', models.DO_NOTHING, db_column='_role', to_field='name', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'form_role'


class FunctionKind(models.Model):
    function_kind_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'function_kind'


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
    direct_inquiry = models.IntegerField(blank=True, null=True)
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


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey('User', models.DO_NOTHING)
    receiver = models.ForeignKey('User', models.DO_NOTHING, related_name='message_receiver_set')
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    reg_dt = models.DateTimeField()
    register = models.IntegerField(blank=True, null=True)
    attachment = models.TextField(blank=True, null=True)
    read_dt = models.DateTimeField(blank=True, null=True)
    close_dt = models.DateTimeField(blank=True, null=True)
    related_message = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message'


class MessageAttachment(models.Model):
    message_attachment_id = models.AutoField(primary_key=True)
    message_id = models.IntegerField()
    session_id = models.CharField(max_length=255)
    filename = models.CharField(max_length=255, blank=True, null=True)
    register = models.IntegerField()
    reg_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'message_attachment'


class Obj(models.Model):
    obj_id = models.AutoField(primary_key=True)
    obj_type = models.ForeignKey('ObjType', models.DO_NOTHING)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obj'


class ObjDocument(models.Model):
    obj_document_id = models.AutoField(primary_key=True)
    source_type = models.CharField(max_length=255)
    source_id = models.IntegerField()
    document_type = models.CharField(max_length=255)
    uri = models.CharField(max_length=255)
    description = models.TextField()
    hash = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'obj_document'


class ObjItem(models.Model):
    obj_item_id = models.AutoField(primary_key=True)
    obj = models.ForeignKey(Obj, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obj_item'


class ObjItemCity(models.Model):
    obj_item_city_id = models.AutoField(primary_key=True)
    obj_item = models.ForeignKey(ObjItem, models.DO_NOTHING)
    city = models.ForeignKey(ObjItem, models.DO_NOTHING, related_name='objitemcity_city_set')

    class Meta:
        managed = False
        db_table = 'obj_item_city'
        db_table_comment = 'هدف از طراحی جدول فوق برای انبارها بوده است\nکه هر انبار به شهرهایی سرویس میدهد و انباردار مربوطه فقط فاکتروهای منطقه خودش را مشاهده کند\nهمپوشانی انبار و منطقه اگر وجود داشته باشد امکان ارسال دوباره کالا خواهد شد'


class ObjItemConfirmer(models.Model):
    obj_item_confirmer_id = models.AutoField(primary_key=True)
    obj_item = models.ForeignKey(ObjItem, models.DO_NOTHING)
    register_chart = models.ForeignKey(Chart, models.DO_NOTHING, blank=True, null=True, db_comment='انبار جارت دریافت کننده\nلوازم مصرفی ثبت کننده و اگر خالی بود همه میتوانند ثبت کنند')
    confirmer_chart = models.ForeignKey(Chart, models.DO_NOTHING, related_name='objitemconfirmer_confirmer_chart_set', blank=True, null=True)
    counter_chart = models.ForeignKey(Chart, models.DO_NOTHING, related_name='objitemconfirmer_counter_chart_set', blank=True, null=True, db_comment='انبار چارت شمارش کننده\nلوازم مصرفی تصویب کننده است و اگر خالی بود تصویب کننده همان تایید کننده می باشد')
    register_hierarchical = models.IntegerField(blank=True, null=True, db_comment='آیا زیر دست های چارت فوق میتوانند ثبت کننده باشند')
    confirmer_hierarchical = models.IntegerField()
    depo_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obj_item_confirmer'
        db_table_comment = 'انبارها\nثثبت کننده\nتایید کننده کیفیت\nشمارش کننده انبار\n\nلوازم مصرفی\nچه کسی صدور میزند اگر خالی بود همه میتوانند صدور بزنند\nچه کسی میتواند این کالا را تایید کند که خریداری شود و نمیتواند خالی باشد\nتصویب کننده اگر تصویب کننده کالا داشت باید تصویب شود وگرنه تایید کننده تصویب کننده هم خواهد بود'


class ObjItemSpec(models.Model):
    obj_item_spec_id = models.AutoField(primary_key=True)
    obj_item = models.ForeignKey(ObjItem, models.DO_NOTHING, blank=True, null=True)
    obj_spec = models.ForeignKey('ObjSpec', models.DO_NOTHING, blank=True, null=True)
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
    obj_type = models.ForeignKey(ObjType, models.DO_NOTHING, blank=True, null=True)
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


class PersonelShift(models.Model):
    personel_shift_id = models.AutoField(primary_key=True)
    person = models.IntegerField(blank=True, null=True)
    shift_id = models.IntegerField(blank=True, null=True)
    start_dt = models.CharField(max_length=10, blank=True, null=True)
    end_dt = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personel_shift'


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
    obj_item = models.ForeignKey(ObjItem, models.DO_NOTHING)
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
    obj_item = models.ForeignKey(ObjItem, models.DO_NOTHING)
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


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role'


class RoleItem(models.Model):
    role_item_id = models.AutoField(primary_key=True)
    field_role = models.ForeignKey(Role, models.DO_NOTHING, db_column='_role', to_field='name', blank=True, null=True)  # Field renamed because it started with '_'.
    field_route = models.CharField(db_column='_route', max_length=100, blank=True, null=True)  # Field renamed because it started with '_'.
    field_pattern = models.CharField(db_column='_pattern', max_length=100, blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'role_item'


class SalaryFactor(models.Model):
    salary_factor = models.OneToOneField('StatementLog', models.DO_NOTHING, primary_key=True)
    rec_type = models.CharField(max_length=7, blank=True, null=True, db_comment='نوع رکورد که ثابت است و از جدول پایه جقوق باید خوانده شود و یا فرمولیک است و باید فرمول محسابه شود')
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    formula = models.TextField(blank=True, null=True)
    kol = models.IntegerField(blank=True, null=True)
    moeen = models.IntegerField(blank=True, null=True)
    tafsily = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salary_factor'


class Shift(models.Model):
    shift_id = models.AutoField(primary_key=True)
    calendar = models.ForeignKey(Calendar, models.DO_NOTHING, blank=True, null=True, db_comment='روزهای تعطیلات شیفت از کدام تقویم گرفته شود')
    name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shift'


class ShiftItem(models.Model):
    shift_item_id = models.AutoField(primary_key=True)
    shift = models.ForeignKey(Shift, models.DO_NOTHING, blank=True, null=True)
    rec_type = models.CharField(max_length=5, blank=True, null=True, db_comment='نوع رکورد استراحت است یا ساعت شیفت')
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shift_item'


class Statement(models.Model):
    statement_id = models.AutoField(primary_key=True)
    person = models.IntegerField(blank=True, null=True)
    salary_factor_id = models.IntegerField(unique=True, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statement'


class StatementAdditional(models.Model):
    statement_additional_id = models.AutoField(primary_key=True)
    person = models.IntegerField(blank=True, null=True)
    month = models.CharField(max_length=10, blank=True, null=True)
    salary_factor_id = models.IntegerField(unique=True, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statement_additional'


class StatementLog(models.Model):
    statement_log_id = models.BigAutoField(primary_key=True)
    person = models.IntegerField(blank=True, null=True)
    month = models.CharField(max_length=7, blank=True, null=True)
    salary_factor_id = models.IntegerField(unique=True, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statement_log'


class Test2(models.Model):
    factor_payway_id = models.IntegerField(primary_key=True)
    factor_id = models.IntegerField()
    pay_level = models.CharField(max_length=7)
    pay_type = models.CharField(max_length=9)
    price = models.FloatField()
    bank_id = models.IntegerField(blank=True, null=True)
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
        db_table = 'test_2'


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    system = models.ForeignKey('TicketSystem', models.DO_NOTHING)
    category = models.ForeignKey('TicketSystemCategory', models.DO_NOTHING)
    status = models.ForeignKey('TicketSystemStatus', models.DO_NOTHING)
    type = models.ForeignKey('TicketSystemType', models.DO_NOTHING)
    source = models.ForeignKey('TicketSystemSource', models.DO_NOTHING)
    priority = models.ForeignKey('TicketSystemPriority', models.DO_NOTHING)
    doer = models.IntegerField(blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    obj_source_id = models.IntegerField(blank=True, null=True)
    obj_source_type = models.CharField(max_length=255, blank=True, null=True)
    voip_id = models.CharField(max_length=255, blank=True, null=True)
    family = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    flag = models.IntegerField()
    files = models.CharField(max_length=255, blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    star = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket'


class TicketAttachment(models.Model):
    ticket_attachment_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255)
    size = models.FloatField(blank=True, null=True)
    uploader = models.IntegerField()
    upload_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_attachment'


class TicketComentRead(models.Model):
    ticket_coment_read = models.AutoField(primary_key=True)
    ticket_comment = models.ForeignKey('TicketComment', models.DO_NOTHING)
    user_id = models.IntegerField()
    view_dt = models.DateTimeField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_coment_read'


class TicketComment(models.Model):
    ticket_comment_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING)
    visiblity = models.CharField(max_length=7, blank=True, null=True, db_comment="If visibility equal to visible then comment's show for requester")
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_comment'


class TicketCommentAttachment(models.Model):
    ticket_comment_attachment = models.AutoField(primary_key=True)
    ticket_comment = models.ForeignKey(TicketComment, models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=True, null=True)
    ext = models.CharField(max_length=10)
    type = models.CharField(max_length=100, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    upload_dt = models.DateTimeField()
    uploader = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ticket_comment_attachment'


class TicketCustomer(models.Model):
    ticket_customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    co_name = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_customer'


class TicketDoer(models.Model):
    ticket_doer_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING)
    doer = models.IntegerField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    leave_dt = models.DateTimeField(blank=True, null=True)
    leave_comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_doer'
        db_table_comment = 'چه افراد دیگری نیز این تیکت نقش دارند\nو چه زمانی خودشان تصمیم گرفته اند از تیکت خارج شوند'


class TicketLog(models.Model):
    ticket_status_log_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_log'
        db_table_comment = 'با هر تغییر در وضعیت تیکت یک لاگ از وضعیت و تغییر دهنده وضعیت در جدول فوق ثبت میگردد'


class TicketSystem(models.Model):
    ticket_system_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    prefix = models.CharField(max_length=25, blank=True, null=True)
    color = models.CharField(max_length=25, blank=True, null=True)
    status = models.CharField(max_length=7, blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system'


class TicketSystemCategory(models.Model):
    ticket_system_category_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    chart_id = models.IntegerField(blank=True, null=True)
    assign_to = models.IntegerField(blank=True, null=True)
    approver = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    send_sms = models.IntegerField()
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    orderby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_category'


class TicketSystemCity(models.Model):
    ticket_system_city = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    city_id = models.IntegerField()
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField(blank=True, null=True)
    chart_id = models.IntegerField(blank=True, null=True, db_comment='بر اساس چارت سازمانی کدام چارت سازمانی وظیفه پاسخ گویی به تیکت های مربوط به شهر انتخاب شده را دارد')

    class Meta:
        managed = False
        db_table = 'ticket_system_city'


class TicketSystemField(models.Model):
    ticket_system_field_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    groupname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    default_value = models.CharField(max_length=255, blank=True, null=True)
    orderby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_field'


class TicketSystemPriority(models.Model):
    ticket_system_priority_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    name = models.CharField(max_length=100, blank=True, null=True)
    orderby = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_priority'


class TicketSystemSource(models.Model):
    ticket_system_source_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    name = models.CharField(max_length=100, blank=True, null=True)
    source_type = models.CharField(max_length=100)
    server = models.CharField(max_length=255, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    orderby = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_source'


class TicketSystemStatus(models.Model):
    ticket_system_status_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50, blank=True, null=True)
    orderby = models.IntegerField(blank=True, null=True)
    need_qc = models.CharField(max_length=3, blank=True, null=True)
    status = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_status'


class TicketSystemTeam(models.Model):
    ticket_system_team_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    owner = models.IntegerField()
    reg_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_team'


class TicketSystemTeamMember(models.Model):
    ticket_system_team_member_id = models.AutoField(primary_key=True)
    ticket_system_team = models.ForeignKey(TicketSystemTeam, models.DO_NOTHING)
    member_id = models.IntegerField()
    register = models.IntegerField()
    reg_dt = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ticket_system_team_member'


class TicketSystemType(models.Model):
    ticket_system_type_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    orderby = models.IntegerField()
    chart_id = models.IntegerField(blank=True, null=True, db_comment='چه عنوان شغلی در چارت سازمانی پاسخ دهنده خواهد بود')
    user_id = models.IntegerField(blank=True, null=True, db_comment='چه کاربری به صورت مستقیم پاسخ گو تیکت های وارده به این بخش خواهد بود')
    register = models.IntegerField()
    reg_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ticket_system_type'


class TicketSystemUser(models.Model):
    ticket_system_user_id = models.AutoField(primary_key=True)
    system = models.ForeignKey(TicketSystem, models.DO_NOTHING)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ticket_system_user'


class TicketTodo(models.Model):
    ticket_todo_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING)
    body = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ticket_todo'


class TicketViewer(models.Model):
    ticket_viewer_id = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING)
    user_id = models.IntegerField()
    register = models.IntegerField(blank=True, null=True)
    reg_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ticket_viewer'


class Tmp(models.Model):
    factor_id = models.IntegerField()
    buyer_id = models.IntegerField()
    contract_id = models.IntegerField(blank=True, null=True)
    vendor = models.IntegerField(blank=True, null=True, db_comment='Vendor buyers')
    factor_item_id = models.IntegerField()
    product_id = models.IntegerField()
    amount_factor = models.FloatField()
    depo_send_id = models.IntegerField(blank=True, null=True)
    goods = models.IntegerField(blank=True, null=True)
    depo_id = models.IntegerField(blank=True, null=True)
    amount_depo_send = models.FloatField(blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    obj_send_id = models.IntegerField(blank=True, null=True)
    action = models.CharField(max_length=7, blank=True, null=True)
    print_id = models.IntegerField(blank=True, null=True)
    print_dt = models.DateTimeField(blank=True, null=True)
    print_desc = models.CharField(max_length=255, blank=True, null=True)
    drive_id = models.IntegerField(blank=True, null=True)
    drive_dt = models.DateTimeField(blank=True, null=True)
    drive_desc = models.CharField(max_length=255, blank=True, null=True)
    drive_status_id = models.IntegerField(blank=True, null=True)
    drive_status_dt = models.DateTimeField(blank=True, null=True)
    drive_status_desc = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp'


class TmpEmpFunction(models.Model):
    person = models.IntegerField(blank=True, null=True)
    dt = models.CharField(max_length=10, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_emp_function'


class TmpShift(models.Model):
    person = models.IntegerField(blank=True, null=True)
    dt = models.CharField(max_length=10, blank=True, null=True)
    shift_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_shift'


class TmpTransTime(models.Model):
    tmp_trans_time_id = models.BigAutoField(primary_key=True)
    person = models.BigIntegerField(blank=True, null=True)
    dt = models.CharField(max_length=10, blank=True, null=True)
    trans_time = models.TimeField(blank=True, null=True)
    rownum = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp_trans_time'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    salt = models.CharField(max_length=255, blank=True, null=True)
    is_otp = models.IntegerField(blank=True, null=True)
    otp = models.CharField(max_length=255, blank=True, null=True)
    vendor_code = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    branch_site = models.CharField(max_length=255, blank=True, null=True)
    internal_phone = models.CharField(max_length=100, blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserChart(models.Model):
    user_chart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    chart = models.ForeignKey(Chart, models.DO_NOTHING, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_chart'


class UserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    field_role = models.ForeignKey(Role, models.DO_NOTHING, db_column='_role', to_field='name', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'user_role'


class UserVendor(models.Model):
    user_vendor_id = models.AutoField(primary_key=True)
    obj_item = models.ForeignKey(ObjItem, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_vendor'
        db_table_comment = 'ارتباط نام کاربری و کد مشتری ثبت شده در سییستم'
