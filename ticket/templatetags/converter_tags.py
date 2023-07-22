from django import template
from persiantools.jdatetime import JalaliDate
from datetime import date,datetime
import random
import pytz
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
            return f"{jalali_date.strftime('%Y-%m-%d')}  |  {time_str}"
        else:
            return jalali_date.strftime("%Y-%m-%d")

    return value

@register.filter
def extract_jalali_parts(value, part):
    if isinstance(value, date):
        jalali_date = JalaliDate(value)
        if part == "year":
            return jalali_date.year
        elif part == "month":
            return jalali_date.month
        elif part == "day":
            return jalali_date.day
    return value
@register.filter
def ticket_index(value):
    # index = str(value.category.ticket_system_category_id) + str(random.randint(10000, 99999))
    # index = len(index)
    # if len(str(index)) > 5 :
    #     index  = index[:-1]
    #     return value.system.prefix + index
    # else:
    #     return value.system.prefix + index
    index = value.category.ticket_system_category_id + random.randint(10000,99999)
    if index > 5 : 
        index = str(index)[:-1]
        return value.system.prefix + index
    else:
        return value.system.prefix + str(index)
# the following code is also possible to implement in the template :
# Year: {{ some_date|extract_jalali_parts:"year" }}
# Month: {{ some_date|extract_jalali_parts:"month" }}
# Day: {{ some_date|extract_jalali_parts:"day" }}
