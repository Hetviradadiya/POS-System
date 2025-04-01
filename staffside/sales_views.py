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

     # Total Sales
    total_sales = Sales.objects.aggregate(total=Sum('total_amount'))['total'] or 0

    # Number of Orders
    num_orders = Sales.objects.count()

    # Get all orders and count items
    order_items = Order.objects.values_list('ordered_items', flat=True)  # Assuming 'items' field stores item names

    # Count occurrences of each item
    item_count = {}
    for order in order_items:
        for item in order.split(', '):  # Assuming items are stored as comma-separated names
            item_count[item] = item_count.get(item, 0) + 1

    # Best-Selling Item
    best_selling_item = max(item_count, key=item_count.get) if item_count else "No Sales Yet"

    sales_data = Sales.objects.all().order_by('-date', '-time')

    context = {
        'total_sales': total_sales,
        'num_orders': num_orders,
        'best_selling_item': best_selling_item,
        "sales_data": sales_data
    }

    return render_page(request, 'staffside/sales.html',context)
