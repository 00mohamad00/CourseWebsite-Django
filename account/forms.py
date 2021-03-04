from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Account


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name','student_id')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)