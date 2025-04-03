from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from adminside.models import*
from adminside.forms import*
from staffside.models import Order,Sales
from datetime import date
from decimal import Decimal



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
                "discount": order.discount,
            }

            # print("orderId:" ,order.order_id)

     # Get logged-in staff details from session
    staff_id = request.session.get("staff_id")
    branch = request.session.get("branch", "Unknown")  # Default to "Unknown" if not found

    if staff_id:
        staff = Staff.objects.filter(staff_id=staff_id).first()
        staff_name = staff.staff_username if staff else "Unknown"
    else:
        staff_name = "Unknown"
     # Handle form submission when "Confirm" is clicked
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        branch = request.session.get("branch")  # Get branch from session
        print("branch_id",branch)
        branch_instance = Branch.objects.get(branch_id=branch)
        if not branch_instance:
            return HttpResponse("No branch assigned", status=400)
        
        discount_value = request.POST.get("discount", "0")  # Get discount from form
        print(f"Discount Received: {discount_value}")
        try:
            discount_value = Decimal(discount_value)  # Convert to Decimal
        except:
            discount_value = Decimal("0")

        # Fetch the order and update status
        try:
            order = Order.objects.get(order_id=order_id)
            order.status = "Done"
            order.discount = discount_value  # Save discount in the order
            order.save()


            # Store order in SalesReport (adminside)
            SalesReport.objects.create(
                order=order,  # Store order reference
                quantity_sold=order.quantity,  
                branch=branch_instance,  # Fetched from session
                customer=order.customer.customer_name if order.customer else "Unknown",
                staff=staff_name,  # Fetched from session
                sale_date=order.created_at,  
            )

            # Delete all cart items for this table
            Cart.objects.filter(table_id=order.table).delete()

            # Store the table_id in session to trigger print after reload
            request.session["print_table_id"] = order.table.table_id

            print("table_id which is send to bill_page",order.table.table_id)

            return redirect(f"/staffside/bill_page/{order.table.table_id}/")  # Reload the page 
        except Order.DoesNotExist:
            pass  # Handle case where order doesn't exist


    branch = request.session.get("branch")  # Get branch from session

    if not branch:
        return HttpResponse("No branch assigned", status=400)

    # Filter orders based on available data
    orders_today = Order.objects.filter(
        created_at__date=today,
        branch=branch
    ).order_by("-created_at")

    context = {
        "orders_by_table": orders_by_table,
        "orders_today" : orders_today,
    }

    return render_page(request, "staffside/orders.html", context)


def bill_page(request, table_id):
    try:
        order = Order.objects.filter(table_id=table_id, status="Done").latest("created_at")

        ordered_items_list = [
            item.split("-") for item in order.ordered_items.split(",") if item
        ]

        total_price = order.price
        discount_value = order.discount
        discount_rate = discount_value / 100  # Convert discount to percentage
        discount = total_price * discount_rate
        gst_rate = Decimal("0.05")  # 5% GST
        gst = (total_price - discount) * gst_rate
        final_total = (total_price - discount) + gst

        branch_id = request.session.get("branch")
        branch = Branch.objects.filter(branch_id=branch_id).first() if branch_id else None
        branch_name = branch.branch_name if branch else "Unknown"
        branch_location = branch.branch_location if branch else "Unknown"
        branch_phone_no = branch.branch_phone_no 

        context = {
            "order": order,
            "ordered_items": ordered_items_list,
            "total_price": total_price,
            "discount_value":discount_value,
            "discount": discount,
            "gst": gst,
            "final_total": final_total,
            "table_id": table_id,
            "now": now(),
            "branch_name": branch_name,
            "branch_location": branch_location,
            "branch_phone_no":branch_phone_no
        }
        return render(request, "staffside/bill_print.html", context)

    except Order.DoesNotExist:
        return HttpResponse("No completed order found for this table", status=404)
