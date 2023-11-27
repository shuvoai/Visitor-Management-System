from django import forms


class DateForm(forms.Form):
    date_start = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control form-control-sm', }))
    date_end = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control form-control-sm', }))
