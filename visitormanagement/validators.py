from django.core.exceptions import ValidationError

import re


def name_validatior(value):
    if not re.match("^[A-Za-z]*[^0-9]*$", value):
        raise ValidationError(
            ('Not a valid name'),
            params={'value': value},
        )
