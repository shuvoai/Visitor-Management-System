from django.core.exceptions import ValidationError

import re


def length_validators(value):
    if not re.match('^.{1,40}$', value):
        raise ValidationError(
            "Visiting Reason can't be more than 40 characters",
            params={'value': value},
        )


# checks if the reason is string only ( no number)
def only_string_validators(value):
    if re.match(r'^\d*$', value):
        raise ValidationError(
            "Visiting Reaon can't be a number.",
            params={'value': value},
        )


def field_required_validators(value):
    if re.match(r"^\s*$", value):
        raise ValidationError(
            "Enter Visiting Reason here.",
            params={'value': value},
        )
