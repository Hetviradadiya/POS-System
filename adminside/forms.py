from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
import re
from adminside.models import*
from django.contrib.auth.hashers import make_password
from phonenumber_field.phonenumber import PhoneNumber
from django import forms

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["branch_name", "branch_location", "branch_area", "branch_phone_no", "branch_status"]


    def clean_branch_phone_no(self):
        phone_no = self.cleaned_data.get("branch_phone_no")

        if isinstance(phone_no, PhoneNumber):  #it's a PhoneNumber object
            phone_no = str(phone_no)  # Convert to string

        # Validate format:
        pattern = r"^\+(1\d{10}|91\d{10}|44\d{9,10}|81\d{9,11}|49\d{10,11}|33\d{9}|61\d{9}|86\d{10,11})$"

        if not re.match(pattern, phone_no):
            raise forms.ValidationError("Enter a valid phone number (e.g., +919876543210).")

        return phone_no
    
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["supplier_name", "supplier_email", "supplier_phone_no", "company_name", "address"]

    def clean_supplier_email(self):
        email = self.cleaned_data.get("supplier_email")
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_pattern, email):
            raise forms.ValidationError("Enter a valid email address (e.g., supplier@example.com).")
        return email
    
    def clean_supplier_phone_no(self):
        phone_no = self.cleaned_data.get("supplier_phone_no")

        if isinstance(phone_no, PhoneNumber):  #it's a PhoneNumber object
            phone_no = str(phone_no)  # Convert to string

        # Validate format:
        pattern = r"^\+(1\d{10}|91\d{10}|44\d{9,10}|81\d{9,11}|49\d{10,11}|33\d{9}|61\d{9}|86\d{10,11})$"

        if not re.match(pattern, phone_no):
            raise forms.ValidationError("Enter a valid phone number (e.g., +919876543210).")

        return phone_no
    
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["food_item", "quantity", "cost_price", "branch", "supplier", "purchased_date", "payment_status"]

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["image", "food_item", "category", "description", "quantity", "branch", "cost_price", "sell_price", "mfg_date", "exp_date"]

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

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            "staff_fullname", "staff_username", "staff_email",
            "staff_password", "staff_phone_no", "staff_img", "staff_role", "branch"
        ]
    
    def clean_staff_email(self):
        email = self.cleaned_data.get("staff_email")
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(email_pattern, email):
            raise forms.ValidationError("Enter a valid email address (e.g., staff24@example.com).")
        return email
    
    def clean_staff_phone_no(self):
        phone_no = self.cleaned_data.get("staff_phone_no")

        if isinstance(phone_no, PhoneNumber):  #it's a PhoneNumber object
            phone_no = str(phone_no)  # Convert to string

        # Validate format:
        pattern = r"^\+(1\d{10}|91\d{10}|44\d{9,10}|81\d{9,11}|49\d{10,11}|33\d{9}|61\d{9}|86\d{10,11})$"

        if not re.match(pattern, phone_no):
            raise forms.ValidationError("Enter a valid phone number (e.g., +919876543210).")

        return phone_no
    
    def save(self, commit=True):
        staff = super().save(commit=False)

        # If updating existing staff
        if staff.pk:
            try:
                existing_staff = Staff.objects.get(pk=staff.pk)
                plain_password = self.cleaned_data["staff_password"]

                # ⚠ Don't rehash if password is already stored correctly
                if not check_password(plain_password, existing_staff.staff_password):
                    staff.staff_password = make_password(plain_password)  # Hash new password
                
                else:
                    staff.staff_password = existing_staff.staff_password  # Keep old hash
                
            except Staff.DoesNotExist:
                staff.staff_password = make_password(self.cleaned_data["staff_password"])
        
        else:
            # New staff, always hash password
            staff.staff_password = make_password(self.cleaned_data["staff_password"])

        if commit:
            staff.save()
        return staff


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Old Password", required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password", required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error("confirm_password", "New password and confirm password do not match.")

        return cleaned_data
    