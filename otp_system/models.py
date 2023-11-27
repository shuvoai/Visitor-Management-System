from django.db import models
from django.utils.translation import gettext_lazy as _
from visitormanagement.models import Visitors
from django.utils import timezone


class OTPManager(models.Manager):
    def generate_visitor_otp(self, visitor):
        pass


class Otp(models.Model):
    otp_code = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text=_('OTP code after hashing'),
        verbose_name=_('OTP code'),
    )
    visitors = models.OneToOneField(
        primary_key=True,
        to=Visitors,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='visitor_otp',
        verbose_name=_('visitor'),
        help_text=_('The visitor associated with this OTP.')
    )
    is_verified = models.BooleanField(
        verbose_name=_('OTP verification status'),
        null=True,
        blank=True,
        default=False
    )
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        auto_now_add=True,
        help_text=_('Timestamp of OTP creation')
    )
    send_at = models.DateTimeField(
        verbose_name=_('send at'),
        null=True,
        blank=True,
        help_text=_('The timestamp of the OTP send to the visitor phone')
    )
    valid_till = models.DateTimeField(
        verbose_name=_('valid till'),
        null=True,
        blank=True,
        help_text=_('The OTP will be valid until this timestamp')
    )
    verified_at = models.DateTimeField(
        verbose_name=_('verified at'),
        null=True,
        blank=True,
        help_text=_('The OTP verified at.')
    )
    objects = OTPManager()

    def __str__(self):
        return self.otp_code + str(self.is_verified)

    class Meta:
        ordering = ['is_verified']
        verbose_name = 'Otp Code'

    def generate_otp(self):
        pass

    def change_is_verified_to_true(self):
        self.is_verified = True
        self.verified_at = timezone.now()
        self.save()
