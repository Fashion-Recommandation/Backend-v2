from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'age']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
