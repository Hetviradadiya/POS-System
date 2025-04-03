from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib import messages
from adminside.models import*
from adminside.forms import*
from staffside.models import Sales,Order
from django.db.models import Sum
from collections import defaultdict
from datetime import date, timedelta
import json


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


def reports(request):
    filter_type = request.GET.get("filter", "all")  # Default to "all"

    # Fetch all sales data without date filter
    if filter_type == "all":
        sales_data = SalesReport.objects.all().order_by("sale_date", "branch", "staff")
    else:
        today = date.today()
        start_date, end_date = today, today

        if filter_type == "monthly":
            start_date = today.replace(day=1)
        elif filter_type == "yearly":
            start_date = today.replace(month=1, day=1)

        sales_data = SalesReport.objects.filter(
            sale_date__date__gte=start_date, sale_date__date__lte=end_date
        ).order_by("sale_date", "branch", "staff")

    # Format sales data
    formatted_sales = [
        {
            "sales_id": sale.sales_id,
            "order_id": sale.order.order_id if sale.order else None,
            "quantity_sold": sale.quantity_sold,
            "branch_name": sale.branch.branch_name if sale.branch else "N/A",
            "customer": sale.customer or "Walk-in",
            "staff": sale.staff,
            "sale_date": sale.sale_date.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for sale in sales_data
    ]

    context = {
        "sales_data": formatted_sales,
        "selected_filter": filter_type,
    }
    return render_page(request, "adminside/reports.html", context)

