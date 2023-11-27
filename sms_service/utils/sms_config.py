from django.conf import settings
SMS_API_URL = "https://esm.aamarpay.dev/sms/api/v1/send-sms/TEST/"
SMS_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Token ' + str(settings.SMS_TOKEN)
}
SMS_PAYLOAD = {
    "sender_id": "8809601010502",
    "remove_duplicate": True
}
