import urllib.request
import urllib.parse

# def send_sms_2273_ir(to, text, true=False):
#     if not SMS_ACTIVE and not true:
#         return False

#     username = SMS_USERNAME
#     password = SMS_PASSWORD
#     sender_number = SMS_FROM
#     text = urllib.parse.quote(text)
#     domain = 'sms1.2273'
    
#     url = f"http://sms1.2273.ir/sendSmsViaURL.aspx?userName={username}&password={password}&domainName={domain}&smsText={text}&reciverNumber={to}&senderNumber={sender_number}"
#     urllib.request.urlopen(url)
#     return True

def send_sms(to, text, true=False):
    # if not SMS_ACTIVE and not true:
    #     return False
    
    # username = 'SMS_USERNAME_NEGAR'
    # password = 'SMS_PASSWORD_NEGAR'
    # sender_number = 'SMS_FROM_NEGAR'
    # message_type = 'SMS_TYPE_NEGAR'
    # text = urllib.parse.quote(text)
    
    # url = f"http://negar.armaghan.net/sms/url_type_message_send.html?username={username}&password={password}&parameters={text}&destination={to}&type={message_type}"
    # urllib.request.urlopen(url)
    return True