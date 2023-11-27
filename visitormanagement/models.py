from django.db import models
from django.contrib.auth.models import User

from django.utils.timezone import now
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timezone
import datetime as dt
import calendar
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import Signal
from department.models import Department
from visitingpurpose.models import VisitingPurpose
from employee.models import Employee
from visitormanagement.validators import name_validatior
from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractMonth
from django.utils import timezone as djangotimezone
# Create your models here.
from django.db.models import Prefetch
signal_for_visitor_token = Signal()


class VisitorManager(models.Manager):
    def visitors_on_site(self):
        return self.filter(visitor_status=Visitors.VisitorStatusChoices.ON_SITE)

    def employees_with_visitors(self):
        employees_with_visitors = self.filter(
            visitor_status=Visitors.VisitorStatusChoices.ON_SITE
        ).values('to_employee__employee_name').annotate(
            visitor_count=Count('to_employee')
        )

        return employees_with_visitors


class Visitors(models.Model):
    class VisitorStatusChoices(models.TextChoices):
        ARRIVED = "ARRIVED", _('Arrived')
        ON_SITE = "ONSITE", _('On-Site')
        WAITING_APPROVAL = 'WAITING_APPROVAL', _('Waiting Approval')
        DEPARTED = 'DEPARTED', _('Departed')
    visitor_date = models.DateTimeField(
        verbose_name=("Creation date"),
        auto_now_add=True,
        null=True
    )
    visitor_name = models.CharField(
        max_length=180,
        validators=[name_validatior]
    )
    visitor_phone_number = PhoneNumberField()
    visitor_email = models.EmailField(
        max_length=254,
        validators=[],
        null=True,
        blank=True
    )
    visitor_organization = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    visitor_address = models.CharField(
        max_length=400
    )
    to_which_department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )
    to_employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )
    visitor_purpose = models.ForeignKey(
        VisitingPurpose,
        on_delete=models.CASCADE
    )
    visitor_status = models.CharField(
        max_length=20,
        verbose_name=_('visitor status'),
        null=True,
        blank=True,
        default=VisitorStatusChoices.ON_SITE,
        choices=VisitorStatusChoices.choices,
        help_text=_(
            'this field denotes whether the visitor is still on the site or left'
        )
    )
    checkout_time = models.DateTimeField(
        verbose_name=_('visitor check-out time'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.visitor_name + str(self.pk)

    def get_total_visitors(self):
        number_of_visitors = Visitors.objects.filter(
            visitor_date__month=now().month
        ).count()
        return number_of_visitors

    def get_previous_month(self):
        today = dt.date.today()
        first = today.replace(day=1)
        last_month = first - dt.timedelta(days=1)
        previous_month = last_month.strftime("%B")
        return previous_month

    def get_visitors_per_month(self):
        current_month = datetime.today().month
        current_year = datetime.today().year
        start_date = datetime(current_year, 1, 1)
        visitors_count = Visitors.objects.filter(
            visitor_date__gte=start_date,
            visitor_date__month__lte=current_month
        ).annotate(
            month=ExtractMonth('visitor_date')
        ).values('month').annotate(
            count=Count('id')
        ).values('month', 'count')

        result = []
        months = range(1, 13)
        for month in months:
            count = 0
            for item in visitors_count:
                if item['month'] == month:
                    count = item['count']
                    break
            result.append((month, count))

        return result

    def get_visitor_change_percentage(self):
        # test = datetime.now().month
        current_month = datetime.now().month
        previous_month = current_month - 1
        year = datetime.now().year
        if previous_month == 0:
            previous_month = 12
            year -= 1

        number_of_visitors_past_month = Visitors.objects.filter(
            visitor_date__year=year,
            visitor_date__month=previous_month
        ).count()
        number_of_visitors = Visitors.objects.filter(
            visitor_date__year=datetime.now().year,
            visitor_date__month=current_month
        ).count()
        change = number_of_visitors - number_of_visitors_past_month
        if change > 0:
            try:
                increment_percentage = (
                    change / number_of_visitors_past_month
                ) * 100
            except ZeroDivisionError:
                increment_percentage = 0
            increment_percentage = round(increment_percentage, 2)
            return increment_percentage

        elif change < 0:
            try:
                decrement_percentage = (
                    change / number_of_visitors_past_month
                ) * 100
            except ZeroDivisionError:
                decrement_percentage = 0
            decrement_percentage = round(
                decrement_percentage, 2
            )
            return decrement_percentage

        else:
            return "Unchanged"

    # codes for visitor token generating signal

    def send_token_generate_signal(self):
        signal_for_visitor_token.send(sender=self.__class__)

    def visitor_checkout(self):
        self.visitor_status = Visitors.VisitorStatusChoices.DEPARTED
        self.checkout_time = djangotimezone.now()
        self.save()

    objects = VisitorManager()

    class Meta:
        ordering = ["-visitor_date"]
        verbose_name = "Visitor data"
        permissions = [
            ("custom_can_add_visitor_form", "can add visitor form"),
        ]
