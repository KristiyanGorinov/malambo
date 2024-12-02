from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from users.models import Users


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True
    )

    password2 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "The passwords do not match. Please try again.")


class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(max_length=13, required=False)
    info = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


