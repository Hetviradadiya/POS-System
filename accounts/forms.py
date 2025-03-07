from django import forms  
from django.contrib.auth.models import User  
from adminside.models import Staff
from django.core.exceptions import ValidationError  
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password


class CustomLoginForm(forms.Form):  
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username or not password:
            self.add_error(None, "Both username and password are required.")
            return

        try:
            staff_user = Staff.objects.get(staff_username=username)

            # Debugging output
            print(f"Stored Password: {staff_user.staff_password}")
            print(f"Entered Password: {password}")

            if not check_password(password, staff_user.staff_password):  
                self.add_error("password", "Incorrect password.")
        
        except Staff.DoesNotExist:
            self.add_error("username", "User does not exist.")
            self.add_error("password", "password is required!")

        return cleaned_data

