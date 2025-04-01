from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from adminside.models import*
from adminside.forms import*
from staffside.models import Order,Sales
from datetime import date

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


def orders(request):
    today = date.today()
    orders_by_table = {}  # Store orders grouped by table
    tables = Table.objects.filter(order__isnull=False).distinct()  # Get tables that have orders

    for table in tables:
        order = Order.objects.filter(table=table, status="pending").first()  # Get latest pending order for the table
        if order:
            # Convert ordered_items string to a list
            ordered_items_list = [
                item.split("-") for item in order.ordered_items.split(",") if item
            ]

            orders_by_table[table.table_id] = {
                "order_id":order.order_id,
                "items": ordered_items_list,
                "price": order.price,
                "quantity": order.quantity,
                "status":order.status,
            }

            # print("orderId:" ,order.order_id)

     # Handle form submission when "Confirm" is clicked
    if request.method == "POST":
        order_id = request.POST.get("order_id")

        # Fetch the order and update status
        try:
            order = Order.objects.get(order_id=order_id)
            order.status = "Done"
            order.save()

            # Create a new sales entry
            sale = Sales.objects.create(
                table=order.table,
                total_amount=order.price,
                payment_method="cash",  # You can add a dropdown in the form to select method
            )
            sale.order_list.add(order)  # Add order to sales
            sale.save()

            # Delete all cart items for this table
            Cart.objects.filter(table_id=order.table).delete()

            return redirect("staffside:orders")  # Reload the page to update the UI
        except Order.DoesNotExist:
            pass  # Handle case where order doesn't exist

    # Filter orders placed today
    orders_today = Order.objects.filter(created_at__date=today).order_by('-created_at')

    context = {
        "orders_by_table": orders_by_table,
        "orders_today" : orders_today,
    }

    return render_page(request, "staffside/orders.html", context)

