from django.core.exceptions import ValidationError

import re


def name_validator(value):
    if not re.match("^[A-Za-z]", value):
        raise ValidationError(
            ("Enter a Valid Department Name"),
            params={"value": value},
        )


def department_details_validator(value):
    if not re.match("^[A-Za-z]", value):
        raise ValidationError(
            ("Enter  Valid Department Details"),
            params={"value": value},
        )


def length_validator(value):
    if not re.match("^.{0,100}$", value):
        raise ValidationError(
            ("Department details cannot contain more than 100 characters.")
        )
