from django import template
from persiantools.jdatetime import JalaliDate
from datetime import date

register = template.Library()

@register.filter
def to_jalali(value):
    if isinstance(value, date):
        jalali_date = JalaliDate(value)
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


# the following code is also possible to implement in the template :
# Year: {{ some_date|extract_jalali_parts:"year" }}
# Month: {{ some_date|extract_jalali_parts:"month" }}
# Day: {{ some_date|extract_jalali_parts:"day" }}
