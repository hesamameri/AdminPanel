from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# class UserManager(BaseUserManager):
#     def create_user(self, username, password=None, **kwargs):
#         user = self.model(username=username, **kwargs)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password=None, **kwargs):
#         kwargs.setdefault('is_staff', True)
#         kwargs.setdefault('is_superuser', True)
#         return self.create_user(username, password, **kwargs)
# class User(AbstractBaseUser):
#     user_id = models.AutoField(primary_key=True)
#     username = models.CharField(unique=True, max_length=255, blank=True, null=True)
#     password = models.CharField(max_length=255, blank=True, null=True)
#     is_otp = models.IntegerField(blank=True, null=True)
#     otp = models.CharField(max_length=255, blank=True, null=True)
#     vendor_code = models.CharField(max_length=255, blank=True, null=True)
#     first_name = models.CharField(max_length=255, blank=True, null=True)
#     last_name = models.CharField(max_length=255, blank=True, null=True)
#     phone = models.CharField(max_length=255, blank=True, null=True)
#     mobile = models.CharField(max_length=255, blank=True, null=True)
#     address = models.CharField(max_length=100, blank=True, null=True)
#     avatar = models.CharField(max_length=255, blank=True, null=True)
#     status = models.IntegerField(blank=True, null=True)
#     name = models.CharField(max_length=100, blank=True, null=True)
#     branch_name = models.CharField(max_length=255, blank=True, null=True)
#     branch_site = models.CharField(max_length=255, blank=True, null=True)
#     internal_phone = models.CharField(max_length=100, blank=True, null=True)
#     session_id = models.CharField(max_length=255, blank=True, null=True)
#     is_active = models.BooleanField(default=True,blank=True)
#     last_login = models.DateTimeField(auto_now=True)
#     objects = UserManager()

#     USERNAME_FIELD = 'username'

#     class Meta:
#         managed = True
#         db_table = 'user'
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
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
    is_active = models.BooleanField(default=True,blank=True)
    last_login = models.DateTimeField(auto_now=True)
    class Meta:
        managed = False
        db_table = 'user'






class UserVendor(models.Model):
    user_vendor_id = models.AutoField(primary_key=True)
    obj_item = models.ForeignKey('ObjItem', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_vendor'
        db_table_comment = 'ارتباط نام کاربری و کد مشتری ثبت شده در سییستم'


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


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role'
class ChartRole(models.Model):
    chart_role_id = models.AutoField(primary_key=True)
    field_role = models.ForeignKey('Role', models.DO_NOTHING, db_column='_role', to_field='name', blank=True, null=True)  # Field renamed because it started with '_'.
    chart = models.ForeignKey(Chart, models.DO_NOTHING, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chart_role'

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


   
class Obj(models.Model):
    obj_id = models.AutoField(primary_key=True)
    obj_type = models.ForeignKey('ObjType', models.DO_NOTHING)
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obj'
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