from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseServerError
from .forms import CustomPasswordChangeForm
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.conf import settings
from django.contrib import messages
from adminside.models import*
from adminside.forms import*
from staffside.models import Sales
import os
import csv
# import codecs

def home(request):
    staff_id = request.session.get("staff_id")  # Get session data
    print(f"Checking session: {staff_id}")

    if not staff_id:
        print("No session found, redirecting to login...")
        return redirect("accounts:loginaccount")  # Redirect if no session found

    try:
        staff_user = Staff.objects.get(staff_id=staff_id)
        print(f"User accessing admin panel: {staff_user.staff_username}, Role: {staff_user.staff_role}, image: {staff_user.staff_img}")

        # Store staff image in session
        if staff_user.staff_img:
            request.session["staff_img"] = f"/media/staff_images/{staff_user.staff_img}"

        else:
            request.session["staff_img"] = None


        if staff_user.staff_role.lower() != "admin":
            print("User is not an admin, redirecting to login...")
            return redirect("accounts:loginaccount")  # Redirect non-admin users
    except Staff.DoesNotExist:
        print("Staff ID not found in database, redirecting to login...")
        return redirect("accounts:loginaccount")

    print("Rendering admin dashboard...")
    return redirect('adminside:dashboard')

from django.contrib.sessions.models import Session

def render_page(request, template, data=None):
    data=data or {}
    # Retrieve session key from URL and apply it
    session_key = request.GET.get("session_key")
    if session_key:
        try:
            session_data = Session.objects.get(session_key=session_key)  # Fetch session
            session_store = request.session.__class__(session_key)  # Load session store
            session_store.load()  # Load session data
            request.session.update(session_store)  # Apply session data to request.session
        except Session.DoesNotExist:
            print("Session not found, using default session.")

    # Debug session data
    # print(f"Current session data in render_page: {request.session.items()}")
    data.update({"template": template, "today_date": now().strftime("%Y-%m-%d"),"staff_username": request.session.get("staff_username", "Guest"),})
    return render(request, "adminside/base.html", data)

def dashboard(request):
    return render_page(request, 'adminside/dashboard.html')

def categories(request):
    if request.method == "POST":
        category_id = request.POST.get("categoryId")  # Get ID 
        category_name = request.POST.get("categoryName", "").strip()
        status = request.POST.get("status") == "on"  # Convert checkbox value to Boolean

        if category_id:  # If ID exists, update category
            category = get_object_or_404(Categories, pk=category_id)
            category.categories_name = category_name
            category.status = status
            category.save()
        else:  # Create new category
            if category_name:
                Categories.objects.create(categories_name=category_name, status=status)

        return redirect("adminside:categories")  

    all_categories = Categories.objects.all()
    return render_page(request, "adminside/categories.html", {"categories": all_categories})

def delete_category(request, category_id):
    try:
        category = get_object_or_404(Categories, pk=category_id)

        # Check if category is linked to any inventory
        related_inventory = Inventory.objects.filter(category=category).exists()
        
        if related_inventory:
            return HttpResponseServerError("Cannot delete category: Related inventory exists.")

        category.delete()  # delete category
        return redirect("adminside:categories")  # redirect to category
    except Exception as e:
        return HttpResponseServerError(f"Error deleting category: {e}")

def tables(request):
    if request.method == "POST":
        # print("Form Data:", request.POST) 
        # table_number = request.POST.get("table_number")
        seats = request.POST.get("seats")
        status = "Vacant"  # Default status

        if not seats:  # Ensure seats is not empty
            # print("not seats selected.")
            messages.error(request, "Please select a table type before adding.")
            return redirect("adminside:tables")

        # Save to Database
        Table.objects.create(seats=seats, status=status)
        # print("Table added with seats:", seats)
        # Redirect back to the tables page to refresh the list
        return redirect("adminside:tables")
    tables = Table.objects.all()

    for table in tables:
        has_orders = Cart.objects.filter(table=table).exists()
        if has_orders:
            table.status = "Occupied"
        elif table.status != "Reserved":
            table.status = "Vacant"

    context = {
        "tables": tables,
    }
    return render_page(request, 'adminside/tables.html', context)

def reports(request):
    sales_data = Sales.objects.all()

    context = {
        'sales_data': sales_data
    }
    return render_page(request, 'adminside/reports.html', context)


def logout_view(request):
    logout(request)
    return redirect('accounts:loginaccount')







