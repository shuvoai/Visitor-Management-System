from django.db import models
from django.utils.translation import gettext_lazy as _
from sms_service.validators import validate_phone_number


class SMSLog(models.Model):
    sms_body = models.TextField(
        verbose_name=_('sms body'),
        max_length=350,
        null=False,
        blank=False,
        help_text=_('The body of the sms that was sent')
    )
    phone_number = models.CharField(
        verbose_name=_('phone number'),
        max_length=15,
        null=False,
        blank=False,
        help_text=_('the phone number to which the sms was sent'),
        validators=[validate_phone_number]
    )
    timestamp = models.DateTimeField(
        verbose_name=_('sms timestamp'),
        help_text=_('the date-time when the sms was sent'),
        auto_now_add=True
    )
    is_delivered = models.BooleanField(
        verbose_name=_('sms delivered'),
        null=True,
        blank=True,
        default=False,
        help_text=_('the sms delivery status')
    )
    api_response = models.JSONField(
        verbose_name=_('api response'),
        null=True,
        blank=True,
        help_text=_(
            'the response data that was sent from the sms delivery api endpoint'
        )
    )

    def __str__(self):
        return str(self.phone_number) + str(self.is_delivered)

    class Meta:
        ordering = ['-timestamp']
