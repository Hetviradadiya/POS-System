from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.utils.timezone import now, timedelta
from django.contrib import messages
from adminside.models import*
from adminside.forms import*
from staffside.models import Sales,Order
from django.db.models import Sum
from collections import Counter
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models.functions import ExtractHour

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

from collections import Counter, defaultdict


def dashboard(request):
    # Total Customers
    total_customers = Customer.objects.count()
    max_customers = 1000
    progress_customers = min((total_customers / max_customers) * 100, 100)

    # Total Orders
    total_orders = Order.objects.count()
    max_orders = 500
    progress_orders = min((total_orders / max_orders) * 100, 100)

    # Filter sales data
    filter_type = request.GET.get("filter", "today")
    sales_data = SalesReport.objects.all()

    if filter_type == "today":
        sales_data = sales_data.filter(sale_date__date=now().date())
    elif filter_type == "monthly":
        sales_data = sales_data.filter(sale_date__year=now().year, sale_date__month=now().month)
    elif filter_type == "yearly":
        sales_data = sales_data.filter(sale_date__year=now().year)

        # Total Profit and Income of the Day
    daily_profit = 0
    today_income = 0
    today = now().date()
    daily_sales_reports = SalesReport.objects.filter(sale_date__date=today)

    for report in daily_sales_reports:
        if report.order and report.order.ordered_items:
            today_income += float(report.order.price)
            items = report.order.ordered_items.split(",")
            for item in items:
                try:
                    name, quantity, selling_price = item.strip().split("-")
                    quantity = int(quantity)
                    selling_price = float(selling_price)

                    inventory_item = Inventory.objects.filter(
                        food_item__food_item__iexact=name.strip()
                    ).select_related("food_item").first()

                    if inventory_item:
                        cost_price = float(inventory_item.food_item.cost_price)
                        profit = (selling_price - cost_price) * quantity
                        daily_profit += profit
                except:
                    continue
    max_profit = 5000  # set your target profit for full bar
    progress_profit = min((daily_profit / max_profit) * 100, 100)

    # Top 5 most sold dishes based on quantity (no threshold)
    dish_counter = Counter()
    dish_prices = {}
    total_sales_count = 0
    staff_sales_count = Counter()

    for sale in sales_data:
        if sale.order and sale.order.ordered_items:
            ordered_items = sale.order.ordered_items.split(",")
            for item in ordered_items:
                parts = item.strip().split("-")
                if len(parts) == 3:
                    dish_name, quantity, price = parts[0].strip(), parts[1].strip(), parts[2].strip()
                    try:
                        quantity = int(quantity)
                        price = float(price)
                    except ValueError:
                        continue
                    dish_counter[dish_name] += quantity
                    total_sales_count += quantity
                    dish_prices[dish_name] = price  # Store latest price
                    staff_sales_count[sale.staff] += quantity

    # Get top 5 dishes
    top_5_dishes = dish_counter.most_common(5)
    trending_dishes = [
        {
            "ordered_items": dish,
            "price": dish_prices.get(dish, 0),
            "count": count
        }
        for dish, count in top_5_dishes
    ]
    # Staff performance
    best_employees = sorted(
        [{"staff_fullname": staff, "order_count": count} for staff, count in staff_sales_count.items()],
        key=lambda x: x["order_count"],
        reverse=True
    )

    # Donut chart - Sales by payment method
    total_income = Sales.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    payment_data = Sales.objects.values('payment_method').annotate(total=Sum('total_amount'))
    sales_data_chart = [[sale['payment_method'], float(sale['total'])] for sale in payment_data]

    # Category-wise sold items
    category_sales = defaultdict(int)
    for sale in sales_data:
        if sale.order and sale.order.ordered_items:
            items = sale.order.ordered_items.split(",")
            for item in items:
                try:
                    name, quantity, price = item.strip().split("-")
                    quantity = int(quantity)
                    inventory_item = Inventory.objects.filter(
                        food_item__food_item__iexact=name.strip()
                    ).select_related('category').first()
                    if inventory_item and inventory_item.category:
                        category_sales[inventory_item.category.categories_name] += quantity
                except:
                    pass

    category_labels = list(category_sales.keys())
    category_values = list(category_sales.values())

    # Daily income chart
    daily_sales = (
        Order.objects.annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(total=Sum('price'))
        .order_by('date')
    )
    sales_dates = [entry['date'].strftime("%Y-%m-%d") for entry in daily_sales]
    sales_totals = [float(entry['total']) for entry in daily_sales]


    # Last 7 Days Orders Chart (date vs total orders)
    last_7_days = now().date() - timedelta(days=6)

    last_7_days_orders = (
        Order.objects.filter(created_at__date__gte=last_7_days)
        .annotate(order_date=TruncDate('created_at'))
        .values('order_date')
        .annotate(order_count=Count('order_id'))
        .order_by('order_date')
    )

    orders_dates = [entry['order_date'].strftime('%Y-%m-%d') for entry in last_7_days_orders]
    orders_counts = [entry['order_count'] for entry in last_7_days_orders]
    
    # Today visitor chart to show which time visitor more come

    today = now().date()
    seven_days_ago = today - timedelta(days=6)

    orders = Order.objects.filter(created_at__date__range=[seven_days_ago, today])

    # Organize data: day name → hour → count
    visits_by_day_hour = defaultdict(lambda: [0]*24)
    for order in orders:
        day_name = order.created_at.strftime("%A")  # e.g., Monday
        hour = order.created_at.hour
        visits_by_day_hour[day_name][hour] += 1

    hour_labels = [f"{h:02d}:00" for h in range(24)]
    colors = [
        "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0",
        "#9966FF", "#FF9F40", "#66D9E8"
    ]
    day_hour_chart_data = [
        {
            "day": day,
            "data": visits_by_day_hour[day],
            "color": colors[i % len(colors)]
        }
        for i, day in enumerate(visits_by_day_hour)
]      
    context = {
        "total_customers": total_customers,
        "progress_customers": progress_customers,
        "total_orders": total_orders,
        "progress_orders": progress_orders,
        "trending_dishes": trending_dishes,
        "employees": best_employees,
        "total_income": total_income,
        "sales_data": sales_data_chart,
        "category_labels": category_labels,
        "category_values": category_values,
        "sales_dates": sales_dates,
        "sales_totals": sales_totals,
        "daily_profit": round(daily_profit, 2),
        "progress_profit": progress_profit,
        "today_income": round(today_income, 2),
        "orders_dates": orders_dates,
        "orders_counts": orders_counts,
        "hour_labels": hour_labels,
        "day_hour_chart_data": day_hour_chart_data,
    }

    return render_page(request, 'adminside/dashboard.html', context)