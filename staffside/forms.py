from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from adminside.models import Customer
from phonenumber_field.phonenumber import PhoneNumber
import re


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["customer_firstname", "customer_email", "customer_phone_no"]

    def clean_customer_email(self):
        email = self.cleaned_data.get("customer_email")
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_pattern, email):
            raise forms.ValidationError("Enter a valid email address (e.g., customer@example.com).")
        return email
    
    def clean_customer_phone_no(self):
        phone_no = self.cleaned_data.get("customer_phone_no")

        if isinstance(phone_no, PhoneNumber):  #it's a PhoneNumber object
            phone_no = str(phone_no)  # Convert to string

        # Validate format:
        pattern = r"^\+(1\d{10}|91\d{10}|44\d{9,10}|81\d{9,11}|49\d{10,11}|33\d{9}|61\d{9}|86\d{10,11})$"

        if not re.match(pattern, phone_no):
            raise forms.ValidationError("Enter a valid phone number (e.g., +919876543210).")

        return phone_no
    
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Old Password'}),
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter New Password'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def clean_new_password1(self):
        password = self.cleaned_data.get("new_password1")

        # Password must be at least 6 characters long
        if len(password) < 6:
            raise forms.ValidationError("❌ Password must be at least 6 characters long.")

        # At least one uppercase letter
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("❌ Password must contain at least one uppercase letter.")

        # At least one digit
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("❌ Password must contain at least one digit.")

        # At least one special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError("❌ Password must contain at least one special character.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        # Check if both passwords match
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("❌ New password and Confirm password do not match.")

        return cleaned_data
    
