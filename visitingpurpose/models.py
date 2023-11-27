from django.db import models
from visitingpurpose.validators import length_validators, only_string_validators, field_required_validators


# Create your models here.
class VisitingPurpose(models.Model):
    purpose_name = models.CharField(max_length=200, validators=[length_validators, only_string_validators, field_required_validators])

    def __str__(self):
        return self.purpose_name

    class Meta:
        ordering = ["-purpose_name"]
        verbose_name = "purpose name"
        permissions = [
            ("custom_can_view_visiting_reason", "can  view visiting reason"),
            ("custom_can_add_visiting_reason", "can  add visiting reason"),
            ("custom_can_update_visiting_reason", "can  update visiting reason"),
            ("custom_can_delete_visiting_reason", "can  delete visiting reason"),
        ]
