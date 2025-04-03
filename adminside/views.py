from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib import messages
from adminside.models import*
from adminside.forms import*
from staffside.models import Sales,Order
from django.db.models import Sum


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
     # Total Customers
    total_customers = Customer.objects.count()
    max_customers = 1000  # Set a reference max value
    progress_customers = min((total_customers / max_customers) * 100, 100)

    # Total Orders
    total_orders = Order.objects.count()
    max_orders = 500  # Set a reference max value
    progress_orders = min((total_orders / max_orders) * 100, 100)

    # Get all orders and count items
    order_items = Order.objects.values_list('ordered_items', flat=True)  
    item_count = {}
    for order in order_items:
        for item in order.split(', '):  
            item_count[item] = item_count.get(item, 0) + 1

    # Trending Dishes
    threshold = total_orders * 0.5  
    trending_dishes = [
        {"name": dish, "count": count}
        for dish, count in sorted(item_count.items(), key=lambda x: x[1], reverse=True)
        if count > threshold
    ]

    # Employees
    employees = Staff.objects.filter(staff_role="staff")

    # **Sales Data for Donut Chart**
    total_income = Sales.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0  
    payment_data = Sales.objects.values('payment_method').annotate(total=Sum('total_amount'))  

    sales_data = [
        [sale['payment_method'], float(sale['total'])] for sale in payment_data
    ]

    context = {
        "total_customers": total_customers,
        "progress_customers": progress_customers,
        "total_orders": total_orders,
        "progress_orders": progress_orders,
        "trending_dishes": trending_dishes,
        "employees": employees,
        "total_income": total_income,  # Pass total income
        "sales_data": sales_data,  # Pass sales data
    }
    return render_page(request, 'adminside/dashboard.html',context)

def logout_view(request):
    logout(request)
    return redirect('accounts:loginaccount')
