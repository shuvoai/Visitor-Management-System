from django.core.exceptions import ValidationError
import re
from django.utils.translation import gettext_lazy as _


def validate_phone_number(value):
    if not re.match(r'^\+?1?\d{9,15}$', value):
        raise ValidationError(
            _('The phone number is not valid.'),
            code='invalid',
            params={
                'value': value
            }
        )


def name_validaotr(value):
    if re.match(r"^\d*$", value):
        raise ValidationError(
            "Team Member name cannot contain numbers.",
            params={'value': value},
        )


def length_validator(value):
    if not re.match("^.{0,50}$", value):
        raise ValidationError(
            "Team Membebr name can't be more than 50 characters.",
            params={"value": value}
        )


def string_validator(value):
    if re.match("^[.!@#$%^&*]", value):
        raise ValidationError(
            "Team Member name is not valid.",
            params={"value": value},
        )


def field_required_validator(value):
    if re.match(r"^\s*$", value):
        raise ValidationError(
            "Must Enter a Team Member Name",
            params={"value": value},

        )


def email_validator(value):
    if not re.match(r"^\w{1,100}@a{2}marpay.com", value):
        raise ValidationError(
            "Enter a valid aamarPay Email Address",
            params={"vaue": value},
        )
