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

# def sales(request):
#     staff_name = request.session.get("staff_username")  # Assuming staff name is stored in session

#     if not staff_name:
#         return render_page(request, 'staffside/sales.html', {'error': 'Staff not logged in'})

#     # Filter SalesReport for this specific staff member
#     sales_data = SalesReport.objects.filter(staff=staff_name).order_by('-sale_date')

#     # Total Sales for this staff
#     total_sales = sales_data.aggregate(total=Sum("order__price"))["total"] or 0  # Assuming price is in the Order model

#     # Number of Orders for this staff
#     num_orders = sales_data.count()

#     # Get all order items for this staff
#     order_items = sales_data.values_list("order__ordered_items", flat=True)

#     # Count occurrences of each item
#     item_count = {}
#     for order in order_items:
#         if order:
#             for item in order.split(", "):  # Assuming items are stored as comma-separated names
#                 item_count[item] = item_count.get(item, 0) + 1

#     # Best-Selling Item
#     best_selling_item = max(item_count, key=item_count.get) if item_count else "No Sales Yet"

#     context = {
#         "total_sales": total_sales,
#         "num_orders": num_orders,
#         "best_selling_item": best_selling_item,
#         "sales_data": sales_data,
#     }

#     return render_page(request, "staffside/sales.html", context)

def sales(request):
    staff_name = request.session.get("staff_username")

    if not staff_name:
        return render_page(request, 'staffside/sales.html', {'error': 'Staff not logged in'})

    # Fetch sales records for the logged-in staff, ordered by date & time
    sales_data = SalesReport.objects.filter(staff=staff_name).order_by("sale_date")

    # Data structure: Date → Time → Customer → Ordered Items + Total Price
    grouped_sales = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"items": defaultdict(int), "total_price": 0})))
    date_rowspans = defaultdict(int)
    time_rowspans = defaultdict(lambda: defaultdict(int))
    customer_rowspans = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    # Step 1: Group sales data
    for sale in sales_data:
        sale_date = sale.sale_date.date()
        sale_time = sale.sale_date.strftime("%H:%M")
        customer_name = sale.customer if sale.customer else "Walk-in"
        order_price = sale.order.price if sale.order and sale.order.price else 0

        if sale.order and sale.order.ordered_items:
            ordered_items = sale.order.ordered_items.split(",")  # Example: "Burger-Small-2, Fries-Medium-1"
            for item in ordered_items:
                parts = item.rsplit("-", 2)  # Split at the last two hyphens
                if len(parts) == 3:
                    product_name, size, quantity = parts
                    try:
                        quantity = int(quantity)
                    except ValueError:
                        quantity = 1
                else:
                    product_name, size = parts[0], "Standard"
                    quantity = 1

                item_key = f"{product_name}-{size}"  # Example: "Burger-Small"
                grouped_sales[sale_date][sale_time][customer_name]["items"][item_key] += quantity  # Sum up quantities

        grouped_sales[sale_date][sale_time][customer_name]["total_price"] += order_price  # Sum total price

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
                total_price = data["total_price"]  # Get total price for this customer at this time

                for product_name, total_quantity in data["items"].items():
                    final_sales_data.append({
                        "sale_date": sale_date,
                        "sale_time": sale_time,
                        "customer_name": customer_name,
                        "product_name": product_name,
                        "total_quantity": total_quantity,
                        "total_price": total_price if product_name == list(data["items"].keys())[0] else None,  # Show price only once per customer
                        "date_rowspan": date_rowspans[sale_date] if sale_time == list(times.keys())[0] and customer_name == list(customers.keys())[0] and product_name == list(data["items"].keys())[0] else 0,
                        "time_rowspan": time_rowspans[sale_date][sale_time] if customer_name == list(customers.keys())[0] and product_name == list(data["items"].keys())[0] else 0,
                        "customer_rowspan": customer_rowspans[sale_date][sale_time][customer_name] if product_name == list(data["items"].keys())[0] else 0,
                    })

    context = {
        "sales_data": final_sales_data,
    }
    return render_page(request, "staffside/sales.html", context)