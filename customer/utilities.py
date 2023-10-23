from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
import urllib.request

def get_object_or_none(model, **kwargs):
    queryset = model.objects.filter(**kwargs)
    if queryset.count() == 0:
        return None
    elif queryset.count() > 1:
        return queryset.last()
    else:
        return queryset.first()
    



# def send_sms_2273_ir(to, text, true=False):
#     if not (SMS_ACTIVE or true):
#         return False

#     username = SMS_USERNAME
#     password = SMS_PASSWORD
#     sender_number = SMS_FROM
#     text = urllib.parse.quote(text)
#     domain = 'sms1.2273'

#     url = f"http://sms1.2273.ir/sendSmsViaURL.aspx?userName={username}&password={password}&domainName={domain}&smsText={text}&reciverNumber={to}&senderNumber={sender_number}"
#     urllib.request.urlopen(url)
#     return True

# def send_sms(to, text, true=False):
#     if not (SMS_ACTIVE or true):
#         return False

#     username = SMS_USERNAME_NEGAR
#     password = SMS_PASSWORD_NEGAR
#     sender_number = SMS_FROM_NEGAR
#     sms_type = SMS_TYPE_NEGAR
#     text = urllib.parse.quote(text)

#     url = f"http://negar.armaghan.net/sms/url_type_message_send.html?username={username}&password={password}&parameters={text}&destination={to}&type={sms_type}"
#     urllib.request.urlopen(url)
#     return True
    


