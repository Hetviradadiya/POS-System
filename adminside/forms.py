from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
import re
from adminside.models import*
from django.contrib.auth.hashers import make_password

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            "staff_fullname", "staff_username", "staff_email",
            "staff_password", "staff_phone", "staff_img", "staff_role", "branch"
        ]

    def save(self, commit=True):
        staff = super().save(commit=False)
        staff.staff_password = make_password(self.cleaned_data["staff_password"])  # Hash password
        if commit:
            staff.save()
        return staff


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
    

