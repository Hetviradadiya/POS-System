from django import forms  
from django.contrib.auth.models import User  
from adminside.models import Staff
from django.core.exceptions import ValidationError  
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
import re


class CustomLoginForm(forms.Form):  
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if not username_or_email or not password:
            self.add_error(None, "Both username/email and password are required.")
            return cleaned_data

        # Determine if it's an email
        is_email = re.match(r"[^@]+@[^@]+\.[^@]+", username_or_email)

        try:
            if is_email:
                staff_user = Staff.objects.get(staff_email=username_or_email)
            else:
                staff_user = Staff.objects.get(staff_username=username_or_email)

            if not check_password(password, staff_user.staff_password):  
                self.add_error("password", "Incorrect password.")
        except Staff.DoesNotExist:
            self.add_error("username", "User does not exist.")
            self.add_error("password", "Password is required.")

        return cleaned_data

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_pattern, email):
            raise forms.ValidationError("Enter a valid email address (e.g., customer@example.com).")

        if not Staff.objects.filter(staff_email=email).exists():
            raise forms.ValidationError("This email is not registered.")
        return email

class OTPForm(forms.Form):
    otp = forms.CharField(
        label='Enter OTP',
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        if not otp.isdigit():
            raise forms.ValidationError("OTP must contain only digits.")
        if len(otp) != 6:
            raise forms.ValidationError("OTP must be exactly 6 digits.")
        return otp

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("new_password")
        p2 = cleaned_data.get("confirm_password")

        # Check empty
        if not p1 or not p2:
            if not p1:
                self.add_error('new_password', "New password is required.")
            if not p2:
                self.add_error('confirm_password', "Confirm password is required.")
            return cleaned_data

        # Check match
        if p1 != p2:
            self.add_error('confirm_password', "Passwords do not match.")
            return cleaned_data

        # Check password strength
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$'
        if not re.match(password_pattern, p1):
            self.add_error(
                'new_password',
                "Password must contain at least 6 characters, one uppercase, one lowercase, one number, and one special character."
            )

        return cleaned_data