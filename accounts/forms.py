from django import forms  
from django.contrib.auth.models import User  
from django.core.exceptions import ValidationError  
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("Username is required.")
        if not User.objects.filter(username=username).exists():
            raise ValidationError("Username does not exist.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Incorrect password.")
        return password