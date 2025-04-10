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
    orders_by_table = {}

    staff_id = request.session.get("staff_id")
    branch_id = request.session.get("branch")

    if not branch_id:
        return HttpResponse("No branch assigned", status=400)

    branch_instance = Branch.objects.filter(branch_id=branch_id).first()
    if not branch_instance:
        return HttpResponse("Invalid branch", status=400)

    # Get only tables with pending orders in the current branch
    tables = Table.objects.filter(
        order__branch=branch_instance,
        order__status="pending"
    ).distinct()

    for table in tables:
        order = Order.objects.filter(
            table=table,
            branch=branch_instance,
            status="pending"
        ).first()
        if order:
            ordered_items_list = [
                item.split("-") for item in order.ordered_items.split(",") if item
            ]

            orders_by_table[table.table_id] = {
                "order_id": order.order_id,
                "items": ordered_items_list,
                "price": order.price,
                "quantity": order.quantity,
                "status": order.status,
                "discount": order.discount,
                "customer": order.customer,
            }

    staff_name = "Unknown"
    if staff_id:
        staff = Staff.objects.filter(staff_id=staff_id).first()
        if staff:
            staff_name = staff.staff_username

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        discount_value = request.POST.get("discount", "0")

        try:
            discount_value = Decimal(discount_value)
        except:
            discount_value = Decimal("0")

        try:
            order = Order.objects.get(order_id=order_id, branch=branch_instance)
            order.status = "Done"
            order.discount = discount_value
            discount_amount = order.price * (discount_value / Decimal("100"))
            order.price = order.price - discount_amount
            order.save()

            for item in order.ordered_items.split(","):
                if item:
                    try:
                        name, quantity, price = item.split("-")
                        quantity = int(quantity)
                    except ValueError:
                        continue

                    purchase = Purchase.objects.filter(
                        food_item=name,
                        branch=branch_instance
                    ).first()
                    if not purchase:
                        continue

                    inventory = Inventory.objects.filter(
                        food_item=purchase,
                        branch=branch_instance
                    ).first()
                    if inventory:
                        inventory.quantity -= quantity
                        inventory.quantity = max(inventory.quantity, 0)
                        inventory.save()

            SalesReport.objects.create(
                order=order,
                quantity_sold=order.quantity,
                branch=branch_instance,
                customer=order.customer,
                staff=staff_name,
            )

            Cart.objects.filter(table_id=order.table).delete()
            request.session["print_table_id"] = order.table.table_id
            return redirect(f"/staffside/bill_page/{order.table.table_id}/")

        except Order.DoesNotExist:
            return HttpResponse("Order not found", status=404)

    #  Get only today's orders from this branch
    orders_today = Order.objects.filter(
        created_at__date=today,
        branch=branch_instance
    ).order_by("-created_at")

    context = {
        "orders_by_table": orders_by_table,
        "orders_today": orders_today,
    }

    return render_page(request, "staffside/orders.html", context)


def bill_page(request, table_id):
    try:
        order = Order.objects.filter(table_id=table_id).latest("created_at")
        branch_id = request.session.get("branch")

        ordered_items_list = []
        total_price = order.price
        discount_value = order.discount
        discount_rate = discount_value / Decimal(100)
        discount = total_price * discount_rate
        gst_rate = Decimal("0.05")
        gst = (total_price - discount) * gst_rate
        final_total = (total_price - discount) + gst

        for item in order.ordered_items.split(","):
            if item:
                try:
                    name, quantity, total_item_price = item.split("-")
                    quantity = int(quantity)
                    total_item_price = Decimal(total_item_price)
                    rate = total_item_price / quantity if quantity else 0
                    amount = total_item_price
                except ValueError:
                    continue

                ordered_items_list.append([name, quantity, rate, amount])
        customer = order.customer
        branch = Branch.objects.filter(branch_id=branch_id).first() if branch_id else None
        branch_name = branch.branch_name if branch else "Unknown"
        branch_location = branch.branch_location if branch else "Unknown"
        branch_phone_no = branch.branch_phone_no if branch else "N/A"

        context = {
            "order": order,
            "customer": customer,
            "ordered_items": ordered_items_list,
            "total_price": total_price,
            "discount_value": discount_value,
            "discount": discount,
            "gst": gst,
            "final_total": final_total,
            "table_id": table_id,
            "now": now(),
            "branch_name": branch_name,
            "branch_location": branch_location,
            "branch_phone_no": branch_phone_no
        }
        return render(request, "staffside/bill_print.html", context)

    except Order.DoesNotExist:
        return HttpResponse("No completed order found for this table", status=404)