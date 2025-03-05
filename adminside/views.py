from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomPasswordChangeForm
from adminside.models import Table
from rest_framework.decorators import api_view
from django.db import connection


def home(request):
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
    sales_data = [
    {"invoice_no": "101", "full_name": "John Doe", "phone": "9876543210", "email": "john.doe@example.com", "total": "450", "paid": "200", "balance": "250", "date": "01/15"},
    
    ]
    return render_page(request, 'adminside/logout.html',data=sales_data)







