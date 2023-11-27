from django.conf import settings
from sms_service.utils.sms_config import SMS_API_URL, SMS_HEADERS, SMS_PAYLOAD
from sms_service.utils.constants import SMSBodyTypes
import requests
import json


class SMSGenerator:
    @staticmethod
    def get_message(**kwargs):
        context = {
            'visitor': kwargs.get('visitor'),
            'otp_code': kwargs.get('otp_code'),
            'visiting_person': kwargs.get('visiting_person'),
            'purpose': kwargs.get('purpose')
        }
        sms_body = SMSBodyTypes[kwargs.get('sms_type')].value.format(
            **context
        )
        return sms_body


class SMSSender(SMSGenerator):
    @staticmethod
    def send_sms(**kwargs):
        payload = SMS_PAYLOAD
        message = SMSGenerator.get_message(**kwargs)
        payload['message'] = message
        payload['receiver'] = kwargs.get('contact_number')
        data_payload = json.dumps(payload)
        response = requests.request(
            "POST",
            SMS_API_URL,
            headers=SMS_HEADERS,
            data=data_payload
        )
        print(response.text)
