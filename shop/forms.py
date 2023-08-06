from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class CustomCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your username"}
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your Email"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter your Password"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm your Password"}
        )
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
