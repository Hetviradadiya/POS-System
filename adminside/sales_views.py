from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib import messages
from adminside.models import *
from adminside.forms import *
from staffside.models import Sales, Order
from django.db.models import Sum
from collections import defaultdict
from datetime import date, timedelta
import json

def render_page(request, template, data=None):
    data = data or {}
    session_key = request.GET.get("session_key")
    if session_key:
        try:
            session_data = Session.objects.get(session_key=session_key)
            session_store = request.session.__class__(session_key)
            session_store.load()
            request.session.update(session_store)
        except Session.DoesNotExist:
            print("Session not found, using default session.")

    data.update({
        "template": template,
        "today_date": now().strftime("%Y-%m-%d"),
        "staff_username": request.session.get("staff_username", "Guest"),
    })
    return render(request, "adminside/base.html", data)

def reports(request):
    filter_type = request.GET.get("filter", "today")
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
    else:
        sales_data = SalesReport.objects.none()

    sales_data = sales_data.order_by("sale_date", "branch", "staff")

    grouped_sales = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))
    date_rowspans = defaultdict(int)
    branch_rowspans = defaultdict(lambda: defaultdict(int))
    staff_rowspans = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for sale in sales_data:
        sale_date = sale.sale_date.date()
        branch_name = sale.branch.branch_name if sale.branch else "N/A"
        staff_name = sale.staff
        items = sale.order.ordered_items.split(",") if sale.order and sale.order.ordered_items else []

        for item in items:
            parts = item.strip().split("-")
            if len(parts) == 3:
                product_name, quantity, _ = parts
                try:
                    quantity = int(quantity)
                except ValueError:
                    quantity = 1
                grouped_sales[sale_date][branch_name][staff_name][product_name] += quantity

    final_sales_data = []

    for sale_date, branches in grouped_sales.items():
        total_date_rows = sum(len(products) for staff_data in branches.values() for products in staff_data.values())
        date_rowspans[sale_date] = total_date_rows

        for branch_name, staff_data in branches.items():
            total_branch_rows = sum(len(products) for products in staff_data.values())
            branch_rowspans[sale_date][branch_name] = total_branch_rows

            for staff_name, products in staff_data.items():
                staff_rowspans[sale_date][branch_name][staff_name] = len(products)

                for idx, (product_name, total_quantity) in enumerate(products.items()):
                    final_sales_data.append({
                        "sale_date": sale_date,
                        "branch_name": branch_name,
                        "staff_name": staff_name,
                        "product_name": product_name,
                        "total_quantity": total_quantity,
                        "date_rowspan": date_rowspans[sale_date] if (
                            branch_name == list(branches.keys())[0] and
                            staff_name == list(staff_data.keys())[0] and
                            idx == 0
                        ) else 0,
                        "branch_rowspan": branch_rowspans[sale_date][branch_name] if (
                            staff_name == list(staff_data.keys())[0] and
                            idx == 0
                        ) else 0,
                        "staff_rowspan": staff_rowspans[sale_date][branch_name][staff_name] if idx == 0 else 0,
                    })

    context = {
        "sales_data": final_sales_data,
        "selected_filter": filter_type,  # ✅ Ensure dropdown reflects the current filter
    }
    return render_page(request, "adminside/reports.html", context)
