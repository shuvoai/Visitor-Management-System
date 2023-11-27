from django import forms

from visitormanagement.models import Visitors
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField


class CustomPhoneNumberPrefixWidget(PhoneNumberPrefixWidget):
    def subwidgets(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        return context['widget']['subwidgets']


class VisitorCreateForm(forms.ModelForm):
    visitor_phone_number = PhoneNumberField(
        region='BD',
        widget=PhoneNumberPrefixWidget(
            country_choices=[
                ("BD", "Bangladesh"),
                ("MY", "Malaysia"),
            ],
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        contact_widgets = self.fields['visitor_phone_number'].widget.widgets
        contact_widgets[0].attrs.update(
            {'class': 'form-select ', 'style': 'width:177px'})
        contact_widgets[1].attrs.update(
            {'class': 'form-control ', 'style': 'width:205px', 'placeholder': "Phone Number"})

    class Meta:
        model = Visitors
        fields = '__all__'
        widgets = {

            'visitor_name': forms.TextInput(attrs={
                'id': "visitor_name",
                'class': 'form-control ',
                'placeholder': " Visitor Name",
                'style': 'width:400px'}
            ),

            'visitor_address': forms.TextInput(attrs={
                'id': "visitor_address",
                'class': 'form-control ',
                'placeholder': "Address",
                'style': 'width:400px'}
            ),

            # 'visitor_phone_number': PhoneNumberPrefixWidget(attrs={'class':'form-control form-control-sm','placeholder':"Phone Number",'style':'width:400px'}),

            # 'visitor_phone_number': CustomPhoneNumberPrefixWidget(),

            'visitor_email': forms.EmailInput(attrs={
                'id': "visitor_email",
                'class': 'form-control ',
                'placeholder': "Email Address",
                'style': 'width:400px'}
            ),
            'visitor_organization': forms.TextInput(attrs={
                'id': "visitor_organization",
                'class': 'form-control ',
                'placeholder': " Visitor organization",
                'style': 'width:400px'}
            ),

            'to_which_department': forms.Select(attrs={
                'id': "to_which_department",
                'autofocus': False,
                'size': 0,
                'style': 'width:400px',
                'placeholder': 'Name',
                'class': 'form-select '}
            ),

            'visitor_purpose': forms.Select(attrs={
                'id': "visitor_purpose",
                'autofocus': False,
                'size': 0,
                'style': 'width:400px',
                'placeholder': 'Name',
                'class': 'form-select '}
            ),

            'to_employee': forms.Select(attrs={
                'id': "to_employee",
                'autofocus': False,
                'size': 0, 'style': 'width:400px',
                'placeholder': 'Name',
                'class': 'form-select '}
            ),

            'employee_email': forms.EmailInput(
                attrs={
                    'id': "employee_email",
                    'class': 'form-control form-control-sm ',
                    'placeholder': "Enter email",
                    'style': 'width:400px'}
            )
        }
