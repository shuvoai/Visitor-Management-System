from django.dispatch import receiver
from django.db.models.signals import post_save
from visitormanagement.models import Visitors
from .models import Otp
from .utils.generate_otp import OTPManager
from django.conf import settings
from sms_service.utils.sms_manager import SMSSender
from sms_service.utils.constants import SMSBodyTypes


@receiver(signal=post_save, sender=Visitors)
def create_otp_code(sender, instance: Visitors, created, **kwargs):
    if created:
        secret_key = settings.OTP_SECRET_KEY
        otp_manager = OTPManager(secret_key)
        generated_otp = otp_manager.generate_random_number()
        encrypted_otp = otp_manager.generate_otp(data=generated_otp)
        Otp.objects.create(
            otp_code=encrypted_otp,
            visitors=instance,
        )


@receiver(signal=post_save, sender=Otp)
def send_sms_to_visitor(sender, instance: Otp, created, **kwargs):
    if created:
        phone_number = instance.visitors.visitor_phone_number
        complete_phone_number = f"{phone_number.country_code}{phone_number.national_number}"
        otp_manager = OTPManager(settings.OTP_SECRET_KEY)
        decrypted_otp = otp_manager.decrypt(instance.otp_code)
        context = {
            'visitor': instance.visitors.visitor_name,
            'otp_code': decrypted_otp,
            'contact_number': complete_phone_number,
            'sms_type': SMSBodyTypes.VISITOR.name
        }
        SMSSender.send_sms(**context)


@receiver(signal=post_save, sender=Otp)
def send_sms_to_visiting_person(sender, instance: Otp, created, **kwargs):
    if created:
        context = {
            'sms_type': SMSBodyTypes.VISITING_PERSON.name,
            'contact_number': instance.visitors.to_employee.phone_number,
            'visiting_person': instance.visitors.to_employee.employee_name,
            'visitor': instance.visitors.visitor_name,
            'purpose': instance.visitors.visitor_purpose.purpose_name
        }
        SMSSender.send_sms(**context)
