from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from adminside.models import*
from adminside.forms import*
from staffside.models import Order,Sales
from django.db.models import Sum
from collections import defaultdict

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
    staff_name = request.session.get("staff_username")

    if not staff_name:
        return render_page(request, 'staffside/sales.html', {'error': 'Staff not logged in'})

    # Fetch sales records for the logged-in staff, ordered by date & time
    sales_data = SalesReport.objects.filter(staff=staff_name).order_by("sale_date")

    # Grouping: Date → Time → Customer → Items + Price
    grouped_sales = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"items": defaultdict(int), "total_price": 0})))
    date_rowspans = defaultdict(int)
    time_rowspans = defaultdict(lambda: defaultdict(int))
    customer_rowspans = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    # Step 1: Group sales data
    for sale in sales_data:
        sale_date = sale.sale_date.date()
        sale_time = sale.sale_date.strftime("%H:%M")
        customer_name = sale.customer.customer_firstname if sale.customer else "-"
        order_price = sale.order.price if sale.order and sale.order.price else 0

        if sale.order and sale.order.ordered_items:
            ordered_items = sale.order.ordered_items.split(",")  # Example: "Burger-2-100,Fries-1-50"
            for item in ordered_items:
                parts = item.strip().split("-")
                if len(parts) == 3:
                    product_name, quantity_str, _ = parts
                    try:
                        quantity = int(quantity_str)
                    except ValueError:
                        quantity = 1
                    grouped_sales[sale_date][sale_time][customer_name]["items"][product_name] += quantity

        grouped_sales[sale_date][sale_time][customer_name]["total_price"] += order_price

    final_sales_data = []

    # Step 2: Compute rowspans
    for sale_date, times in grouped_sales.items():
        total_date_rows = sum(len(data["items"]) for customers in times.values() for data in customers.values())
        date_rowspans[sale_date] = total_date_rows

        for sale_time, customers in times.items():
            total_time_rows = sum(len(data["items"]) for data in customers.values())
            time_rowspans[sale_date][sale_time] = total_time_rows

            for customer_name, data in customers.items():
                customer_rowspans[sale_date][sale_time][customer_name] = len(data["items"])
                total_price = data["total_price"]

                for idx, (product_name, total_quantity) in enumerate(data["items"].items()):
                    final_sales_data.append({
                        "sale_date": sale_date,
                        "sale_time": sale_time,
                        "customer_name": customer_name,
                        "product_name": product_name,
                        "total_quantity": total_quantity,
                        "total_price": total_price if idx == 0 else None,  # Show price only once per customer
                        "date_rowspan": date_rowspans[sale_date] if (
                            sale_time == list(times.keys())[0] and
                            customer_name == list(customers.keys())[0] and
                            idx == 0
                        ) else 0,
                        "time_rowspan": time_rowspans[sale_date][sale_time] if (
                            customer_name == list(customers.keys())[0] and
                            idx == 0
                        ) else 0,
                        "customer_rowspan": customer_rowspans[sale_date][sale_time][customer_name] if idx == 0 else 0,
                    })

    context = {
        "sales_data": final_sales_data,
    }
    return render_page(request, "staffside/sales.html", context)