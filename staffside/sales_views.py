from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from adminside.models import*
from adminside.forms import*
from staffside.models import Order,Sales
from django.db.models import Sum

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

def sales(request):
    staff_name = request.session.get("staff_username")  # Assuming staff name is stored in session

    if not staff_name:
        return render_page(request, 'staffside/sales.html', {'error': 'Staff not logged in'})

    # Filter SalesReport for this specific staff member
    sales_data = SalesReport.objects.filter(staff=staff_name).order_by('-sale_date')

    # Total Sales for this staff
    total_sales = sales_data.aggregate(total=Sum("order__price"))["total"] or 0  # Assuming price is in the Order model

    # Number of Orders for this staff
    num_orders = sales_data.count()

    # Get all order items for this staff
    order_items = sales_data.values_list("order__ordered_items", flat=True)

    # Count occurrences of each item
    item_count = {}
    for order in order_items:
        if order:
            for item in order.split(", "):  # Assuming items are stored as comma-separated names
                item_count[item] = item_count.get(item, 0) + 1

    # Best-Selling Item
    best_selling_item = max(item_count, key=item_count.get) if item_count else "No Sales Yet"

    context = {
        "total_sales": total_sales,
        "num_orders": num_orders,
        "best_selling_item": best_selling_item,
        "sales_data": sales_data,
    }

    return render_page(request, "staffside/sales.html", context)
