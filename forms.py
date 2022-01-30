from django.forms import ModelForm
from .models import CaUser
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = forms.TextInput(attrs={'class': 'form-control', 'palceholder': '', 'id': 'hello'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'palceholder': '', 'id': 'hi'}))


class CASignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CaUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.save()
        return user
