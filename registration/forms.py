from django import forms

from registration.models import Registration


class RegisterBaseForm(forms.ModelForm):
    class Meta:
        model = Registration
        exclude = ('user', 'competition',)
