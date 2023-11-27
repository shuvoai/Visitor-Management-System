from django import forms

from .models import VisitingPurpose


class VisitingPurposeForm(forms.ModelForm):
    class Meta:
        model = VisitingPurpose
        fields = '__all__'
        widgets = {
            'purpose_name': forms.TextInput(attrs={'placeholder': 'Visiting Purpose', 'class': 'w-100 rounded p-2'}),

        }


class VisitingPurposeUpdateForm(forms.ModelForm):
    class Meta:
        model = VisitingPurpose
        fields = '__all__'
        widgets = {
            'purpose_name': forms.TextInput(attrs={'placeholder': 'Visiting Purpose', 'class': 'w-100 rounded p-2'}),

        }
