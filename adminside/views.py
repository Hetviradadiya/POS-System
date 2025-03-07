from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomPasswordChangeForm
from adminside.models import*
from rest_framework.decorators import api_view
from django.db import connection
from django.contrib import messages
from adminside.models import*
from adminside.forms import*


def home(request):
    staff_id = request.session.get("staff_id")  # Get session data
    print(f"Checking session: {staff_id}")

    if not staff_id:
        print("No session found, redirecting to login...")
        return redirect("login")  # Redirect if no session found

    try:
        staff_user = Staff.objects.get(staff_id=staff_id)
        print(f"User accessing admin panel: {staff_user.staff_username}, Role: {staff_user.staff_role}")

        if staff_user.staff_role.lower() != "admin":
            print("User is not an admin, redirecting to login...")
            return redirect("login")  # Redirect non-admin users
    except Staff.DoesNotExist:
        print("Staff ID not found in database, redirecting to login...")
        return redirect("login")

    print("Rendering admin dashboard...")
    return redirect('adminside:dashboard')

def render_page(request, template, data=None):
    return render(request, "adminside/base.html", {"template": template, "data":data})

def dashboard(request):
    return render_page(request, 'adminside/dashboard.html')

def branches(request):   
    return render_page(request, 'adminside/branches.html')

def suppliers(request):
    return render_page(request, 'adminside/suppliers.html')

def purchase(request):    
    return render_page(request, 'adminside/purchase.html')

def categories(request):
    return render_page(request, 'adminside/categories.html')

def inventory(request):
    return render_page(request, 'adminside/inventory.html')

def fooditems(request):
    return render_page(request, 'adminside/fooditems.html')

def tables(request):
    return render_page(request, 'adminside/tables.html')

def customer(request):
    return render_page(request, 'adminside/customer.html')

def staff(request):
    if request.method == "POST":
        staff_fullname = request.POST.get("fullName")
        staff_username = request.POST.get("userName")
        staff_email = request.POST.get("email")
        staff_password = request.POST.get("password")
        staff_role = request.POST.get("staffRole")
        branch_name = request.POST.get("branches")
        staff_image = request.FILES.get("staffImage")  # Handle image upload

        # Validate required fields
        if not all([staff_fullname, staff_username, staff_email, staff_password, staff_role, branch_name]):
            messages.error(request, "All fields are required.")
            return redirect("adminside:staff")

        # Check if username already exists
        if Staff.objects.filter(staff_username=staff_username).exists():
            messages.error(request, "Username already taken. Please choose another.")
            print("Username already taken. Please choose another.")
            return redirect("adminside:staff")

        # Save staff to database
        staff_member = Staff(
            staff_fullname=staff_fullname,
            staff_username=staff_username,
            staff_email=staff_email,
            staff_password=make_password(staff_password),  # Hash password
            staff_role=staff_role,
            branch=branch,
            staff_img=staff_image  # Save uploaded image
        )
        staff_member.save()

        messages.success(request, "Staff member added successfully!")
        print("Staff member added successfully!")
        return redirect("adminside:staff")  # Redirect to prevent duplicate form submissions

    # Fetch existing staff list
    staff_list = Staff.objects.all()

    # return render(request, "adminside/staff.html", {"staff_list": staff_list})
    return render_page(request, 'adminside/staff.html')

def reports(request):
    sales_data = [
    {"product_id": "101", "product_name": "Neapolitan Pizaa", "calegories": "Pizaa", "email": "john.doe@example.com", "quentity": "450", "paid": "200", "balance": "250", "date": "01/15"},
    {"product_id": "102", "product_name": "Veg. Burger", "calegories": "Burger", "email": "jane.smith@example.com", "quentity": "350", "paid": "150", "balance": "200", "date": "01/16"},
    {"product_id": "103", "product_name": "French Fries", "calegories": "Fast Food", "email": "robert.brown@example.com", "quentity": "500", "paid": "250", "balance": "250", "date": "01/17"},
    {"product_id": "104", "product_name": "Veg. Sandvich", "calegories": "Sandvich", "email": "emily.white@example.com", "quentity": "600", "paid": "300", "balance": "300", "date": "01/18"},
    {"product_id": "105", "product_name": "Dosa (Butter)", "calegories": "South Indian", "email": "michael.green@example.com", "quentity": "750", "paid": "500", "balance": "250", "date": "01/19"},
    ]
    return render_page(request, 'adminside/reports.html', data=sales_data)


def adminside_settings_view(request):
    return redirect('adminside:profile')

def render_settings_page(request, template, context=None):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, template, context or {})
    context = context or {}
    context["template"] = template  # Ensures `template` is still passed
    return render(request, "adminside/settings.html", context)

def change_password(request):
    form = CustomPasswordChangeForm(request.user)
    return render_settings_page(request, "adminside/settings/change_password.html", {'form': form})

def edit_profile(request):
    return render_settings_page(request,"adminside/settings/edit_profile.html")

def profile(request):
    return render_settings_page(request,"adminside/settings/profile.html")

def logout_view(request):
    return redirect('accounts:loginaccount')







