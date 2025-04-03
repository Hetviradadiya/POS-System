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
    filter_type = request.GET.get("filter", "all")
    today = date.today()
    
    # Filtering logic
    if filter_type == "all":
        sales_data = SalesReport.objects.all()
    elif filter_type == "today":
        sales_data = SalesReport.objects.filter(sale_date__date=today)
    elif filter_type == "monthly":
        sales_data = SalesReport.objects.filter(sale_date__year=today.year, sale_date__month=today.month)
    elif filter_type == "yearly":
        sales_data = SalesReport.objects.filter(sale_date__year=today.year)

    sales_data = sales_data.order_by("sale_date", "branch", "staff")

    grouped_sales = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))
    date_rowspans = defaultdict(int)
    branch_rowspans = defaultdict(lambda: defaultdict(int))
    staff_rowspans = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    # Step 1: Group sales data by date → branch → staff → product
    for sale in sales_data:
        sale_date = sale.sale_date.date()
        branch_name = sale.branch.branch_name if sale.branch else "N/A"
        staff_name = sale.staff
        items = sale.order.ordered_items.split(",")

        for item in items:
            product_name = item.split("-")[0]
            grouped_sales[sale_date][branch_name][staff_name][product_name] += 1

    final_sales_data = []

    # Step 2: Compute rowspans
    for sale_date, branches in grouped_sales.items():
        total_date_rows = sum(len(products) for staff_data in branches.values() for products in staff_data.values())
        date_rowspans[sale_date] = total_date_rows

        for branch_name, staff_data in branches.items():
            total_branch_rows = sum(len(products) for products in staff_data.values())
            branch_rowspans[sale_date][branch_name] = total_branch_rows

            for staff_name, products in staff_data.items():
                staff_rowspans[sale_date][branch_name][staff_name] = len(products)

                for product_name, total_quantity in products.items():
                    final_sales_data.append({
                        "sale_date": sale_date,
                        "branch_name": branch_name,
                        "staff_name": staff_name,
                        "product_name": product_name,
                        "total_quantity": total_quantity,
                        "date_rowspan": date_rowspans[sale_date] if branch_name == list(branches.keys())[0] and staff_name == list(staff_data.keys())[0] and product_name == list(products.keys())[0] else 0,
                        "branch_rowspan": branch_rowspans[sale_date][branch_name] if staff_name == list(staff_data.keys())[0] and product_name == list(products.keys())[0] else 0,
                        "staff_rowspan": staff_rowspans[sale_date][branch_name][staff_name] if product_name == list(products.keys())[0] else 0,
                    })

    context = {
        "sales_data": final_sales_data,
    }
    return render_page(request, "adminside/reports.html", context)