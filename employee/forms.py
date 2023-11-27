from django import forms

from .models import Employee


class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'department': forms.Select(attrs={'autofocus': False, 'size': 0, 'placeholder': 'Name', 'class': 'w-100 rounded p-2'}),

            'employee_name': forms.TextInput(attrs={'class': 'w-100 rounded p-2', 'placeholder': "Enter Employee", }),

            'employee_email': forms.EmailInput(attrs={'class': 'w-100 rounded p-2', 'placeholder': "Enter email"}),
            'phone_number': forms.TextInput(attrs={'class': 'w-100 rounded p-2', 'placeholder': "Enter Phone Number"}),
        }


class EmployeeUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'department': forms.Select(attrs={'autofocus': False, 'size': 0, 'style': 'width:400px', 'placeholder': 'Name', 'class': 'form-control form-control-sm'}),

            'employee_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': "Enter Employee", 'style': 'width:400px'}),

            'employee_email': forms.EmailInput(attrs={'class': 'form-control form-control-sm ', 'placeholder': "Enter email", 'style': 'width:400px'}),

            'phone_number': forms.TextInput(attrs={'class': 'form-control form-control-sm ', 'placeholder': "Enter Phone Number", 'style': 'width:400px'}),
        }
