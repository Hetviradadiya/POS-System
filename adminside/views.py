from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.utils.timezone import now,timezone
from django.contrib import messages
from adminside.models import*
from adminside.forms import*
from staffside.models import Sales,Order
from django.db.models import Sum
from collections import Counter
from django.db.models import Count
from django.db.models.functions import TruncDate


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

        today = timezone.now().date()

        if staff_user.staff_role.lower() == "admin":
            expired_items = Inventory.objects.filter(
                expiry_date__lt=today
            ).values("food_item", "exp_date", "branch__branch")
        else:  # For manager, show only their branch's expired items
            expired_items = Inventory.objects.filter(
                expiry_date__lt=today,
                branch_id=staff_user.branch
            ).values("food_item", "exp_date")

        print("expiered_items",expired_items)
        request.session["expired_items"] = list(expired_items)
        request.session["today_date"] = str(today)

        if staff_user.staff_role.lower() != "admin":
            print("User is not an admin, redirecting to login...")
            return redirect("accounts:loginaccount")  # Redirect non-admin users
    except Staff.DoesNotExist:
        print("Staff ID not found in database, redirecting to login...")
        return redirect("accounts:loginaccount")

    print("Rendering admin dashboard...")
    return redirect('adminside:dashboard')

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


def logout_view(request):
    logout(request)
    return redirect('accounts:loginaccount')
