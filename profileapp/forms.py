from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    first_name = forms.CharField(max_length=30, required=False, label="First Name", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your first name'
    }))
    last_name = forms.CharField(max_length=30, required=False, label="Last Name", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your last name'
    }))
    telegram_id = forms.CharField(max_length=50, required=True, label="Telegram ID", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Telegram ID'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'telegram_id', 'password1', 'password2']
