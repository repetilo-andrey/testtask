from django import forms
from django.utils import timezone

from coworkers.models import Coworker


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class CoworkerForm(forms.ModelForm):
    class Meta:
        model = Coworker
        fields = ['pib', 'position', 'start_date', 'email', 'parent']

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date > timezone.now().date():
            raise forms.ValidationError("Start date cannot be in the future.")
        return start_date
