from django import template
from persiantools.jdatetime import JalaliDate
from datetime import date,datetime
import random
import pytz

from Administrator.models import User
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
def register_user(value):
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
    return int(number)