from django import forms

from .models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'department_description': forms.Textarea(attrs={'rows': 3, 'placeholder': "Details", 'class': 'w-100 rounded p-2'}),
            'department_name': forms.TextInput(attrs={'placeholder': "Department", 'class': 'w-100 rounded p-2'})
        }


class DepartmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'department_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control form-control-sm', 'placeholder': "Details", 'style': 'width:400px'}),
            'department_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': "Department", 'style': 'width:400px'})
        }
