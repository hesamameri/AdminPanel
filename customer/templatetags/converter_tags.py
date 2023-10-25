from django import template
from persiantools.jdatetime import JalaliDate
from datetime import date,datetime
import random
import pytz

from Administrator.models import User
from customer.models import ObjItem
register = template.Library()

@register.filter
def to_jalali(value):
    if isinstance(value, (date, datetime)):
        tz = pytz.timezone('Asia/Tehran')  # Set the timezone to Iran/Tehran
        value_tehran = value.astimezone(tz)

        jalali_date = JalaliDate(value_tehran)

        if isinstance(value, datetime):
            # If the input is a datetime object, include the time in the Jalali date string
            time_str = value_tehran.strftime("%H:%M:%S")
            return f"{jalali_date.strftime('%Y-%m-%d')}"
        else:
            return jalali_date.strftime("%Y-%m-%d")

    return value


@register.filter
def extract_time(value):
    if isinstance(value, datetime):
        return value.strftime("%H:%M:%S")
    return value


@register.filter
def register_user(value):
    if value == 1 :
        return "نامشخص"
    else:

        user = User.objects.get(user_id = value)

    return user.name


@register.filter
def nth_item(queryset, counter):
    try:
        return queryset[counter]
    except IndexError:
        return None
@register.filter
def inter(number):
    if not isinstance(number, str):
        number = str(number)

    # Convert to float first, then to int
    try:
        number = int(float(number))
    except ValueError:
        return "Invalid number"

    number_str = str(number)

    # Check if the negative sign is at the end and move it to the front
    if number_str.endswith('-'):
        number_str = '-' + number_str[:-1]

    return number_str

@register.filter
def city_rec(id):
    try:
        city = ObjItem.objects.get(obj_item_id=id)
        return city.name
    except ObjItem.DoesNotExist:
        return ""
    
@register.filter
def subtract_items(item,item2):
    item = int(item)
    item2 = int(item2)
    return (item - item2)


@register.filter
def id_to_city(item):
    item=str(item) 
    id_dic = {
        '999002001':'سبزوار',
        '999002002':'تهران','999001002':'تهران',
        '999002003':'کرج',
        '999002024':'اسفراین',

        }
    if item in id_dic.keys():
            return id_dic[item]
    else:
        return ""
    
@register.filter(name='get_attribute')
def get_attribute(obj, attribute_name):
    return getattr(obj, attribute_name, None)


@register.filter(name='add')
def custom_add(value, arg):
    return value + arg

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.simple_tag
def multiply_and_subtract(num1, num2, subtract_value):
    return (num1 * num2) - subtract_value

@register.filter
def pay_to_way(value):
    items = {
        'CASH':'نقدی',
        'CHEQUE':'چک',
        'CREDIT':'اعتباری',
        'OTHER':'سایر',
        'CARTOCART':'کارت به کارت',
        'REBATE':'تخفیف',
        'ATHOME':'درب منزل',
        'WITHACC':'تسویه با مالی',
        'CART':'کارتخوان',
    }
    if items[value] != None:
        return items[value]
    else:
        return ""

@register.filter
def depo_location(item):
    item = item.lower()
    depos = {

        'shahriar': 'انبار شهریار',
        'product': 'محصول',
        'install': 'نصب',
        'drive': 'حمل',
        'beyhagh' : 'بیهق دوام'
    }
    return depos[item]


@register.filter
def insert_slashes(value):
    value = str(value)
    if len(value) >= 7:
        return value[:5] + '/' + value[5:7] + '/' + value[7:]
    
    elif len(value) >= 5:
        return value[:5] + '/' + value[5:]
    else:
        return value
@register.filter
def inquiry_translate(value):
    items = {
        'COND_CONFIRM':'تایید مشروط',
        'CONFIRM':'تایید',
        'REJECT':'رد',
        'BACK':'برگشتی',
        
    }
    if items[value] != None:
        return items[value]
    else:
        return value
    
@register.filter(name='get_range') 
def get_range(number):
    return range(1,number+1)

@register.filter
def id_to_bank(item):
    item=str(item) 
    id_dic = {
        '999003010':'سپه',
        '999003011':'ملی 3003-1820',
        '999003012':'ملی 67000-9211',
        '999003013':'ملی',
        '999003014':'شهر',
        '999003015':'کشاورزی',
        '999003016':'سامان',
        '999003017':'ملت',
        '999003018':'رسالت',
        '999003019':'پست بانک ایران',


        }
    if item in id_dic.keys():
            return id_dic[item]
    else:
        return ""


@register.filter
def financial_approval_access(id):
    finance_approval_access = [5,4]
    if id == finance_approval_access:
        return True
    else:
        return False
    
@register.filter
def final_register_access(id):
    
    final_register_access = [9 ,21, 37, 4]
    if id in final_register_access:
        return True
    else:
        return False
    
@register.filter
def sales_register_access(id):
    
    final_register_access = [21, 37]
    if id in final_register_access:
        return True
    else:
        return False
    

@register.filter
def goods_register_access(id):
    
    final_register_access = [4, 9]
    if id in final_register_access:
        return True
    else:
        return False
    
@register.filter
def name_to_type(item):
    item=str(item) 
    id_dic = {
        'CASH':'نقدی',
        'CARTOCART':'کارت به کارت',
        'CHEQUE':'چک',
        'CART':'کارت خوان',

        }
    if item in id_dic.keys():
            return id_dic[item]
    else:
        return ""
    
@register.filter
def driveid_to_drivename(item):
    item=str(item) 
    id_dic = {
        '4012001':'حسن عاقلی',
        '4012003':'حمل با مشتری',
        '4012008':'شهاب محسنی',
        '4012009':'علی سعیدی',
        '4012010':'محمد نوری',
        '4012011':'فرهاد چنگی',
        '4012012':'امیر دیواندری',
        '4012013':'اسنپ',
        '4012014':'جلال علی آبادی',
        }
    if item in id_dic.keys():
            return id_dic[item]
    else:
        return ""
    

@register.filter
def installid_to_drivename(item):
    item=str(item) 
    id_dic = {
        '4011001':'قاسمپور',
        '4011007':'عباس دولت آبادی',
        '4011011':'محسن شهابی',
        '4011013':'حسن عاقلی',
        '4011017':'بدون نصب',
        '4011019':'حسین بروغنی',
        '4011020':'مصطفی مهری',
        '4011021':'هادی رجایی ',
        '4011022':'سید مهدی نیکپور ریوندی',
        '4011023':'محمد افچنگی',
        '4011024':'جواد میان آبادی',
        '4011025':'رزرو',
        '4011026':'مصطفی دلاوری',
        '4011028':'اسماعیل نورنهنگ',
        '4011029':'میلاد ثابت',
        '4011030':'علی قاسمی',
        '4011031':'عباس خسروجردی',
        '4011032':'سعید مشکانی',
        '4011033':'مهرداد پاکیشان',
        '4011034':'میلاد بینش',
        '4011035':'علیرضا کرمی',
        '4011036':'امیرحسین نقدی',
        '4011037':'امیر عادلی',
}
    if item in id_dic.keys():
            return id_dic[item]
    else:
        return ""