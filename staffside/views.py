from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseServerError
from .forms import CustomPasswordChangeForm
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from adminside.models import*
from adminside.forms import*
from staffside.models import Order,Sales
from django.db.models import Sum
from datetime import date

def home(request):
    staff_id = request.session.get("staff_id")  # Get session data
    print(f"Checking session: {staff_id}")

    if not staff_id:
        print("No session found, redirecting to login...")
        return redirect("accounts:loginaccount")  # Redirect if no session found

    try:
        staff_user = Staff.objects.get(staff_id=staff_id)
        print(f"User accessing admin panel: {staff_user.staff_username}, Role: {staff_user.staff_role}")

        # Store staff image in session
        if staff_user.staff_img:
            request.session["staff_img"] = f"/media/staff_images/{staff_user.staff_img}"

        else:
            request.session["staff_img"] = None


        if staff_user.staff_role.lower() != "admin":
            return redirect("accounts:loginaccount")  # Redirect non-admin users
        
        print(f"Stored Staff Image: {request.session.get('staff_img')}")
        print(f"Stored Username: {request.session.get('staff_username')}")
        
    except Staff.DoesNotExist:
        print("Staff ID not found in database, redirecting to login...")
        return redirect("accounts:loginaccount")
    
    return redirect('staffside:pos')

def render_page(request, template, data=None):
    data=data or {}
    session_key = request.GET.get("session_key")
    if session_key:
        try:
            session_data = Session.objects.get(session_key=session_key)  # Fetch session
            session_store = request.session.__class__(session_key)  # Load session store
            session_store.load()  # Load session data
            request.session.update(session_store)  # Apply session data to request.session
        except Session.DoesNotExist:
            print("Session not found, using default session.")
    data.update({"template": template, "today_date": now().strftime("%Y-%m-%d"),"staff_username": request.session.get("staff_username", "Guest"),})
    return render(request, "staffside/base.html", data)

from decimal import Decimal

def bill_page(request, table_id):
    cart_items = Cart.objects.filter(table_id=table_id)
    total_price = sum(item.price * item.quantity for item in cart_items)
    
    discount_rate = Decimal("0.10")  # Convert to Decimal
    gst_rate = Decimal("0.07")       # Convert to Decimal

    discount = total_price * discount_rate  # Ensure Decimal * Decimal
    gst = (total_price - discount) * gst_rate  # Ensure Decimal * Decimal
    final_total = (total_price - discount) + gst  # Ensure all are Decimals


    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "discount": discount,
        "gst": gst,
        "final_total": final_total,
        "table_id": table_id
    }
    return render(request, "staffside/bill_print.html", context)

def logout_view(request):
    return redirect('accounts:loginaccount')

