from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseServerError
from .forms import CustomPasswordChangeForm
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from adminside.models import*
from adminside.forms import*
from staffside.models import Order,Sales
from django.db.models import Sum
from datetime import date

def home(request):
    staff_id = request.session.get("staff_id")  # Get session data
    print(f"Checking session: {staff_id}")

    if not staff_id:
        print("No session found, redirecting to login...")
        return redirect("accounts:loginaccount")  # Redirect if no session found

    try:
        staff_user = Staff.objects.get(staff_id=staff_id)
        print(f"User accessing admin panel: {staff_user.staff_username}, Role: {staff_user.staff_role}")

        # Store staff image in session
        if staff_user.staff_img:
            request.session["staff_img"] = staff_user.staff_img.url
        else:
            request.session["staff_img"] = None

        if staff_user.staff_role.lower() != "admin":
            return redirect("accounts:loginaccount")  # Redirect non-admin users
        
        print(f"Stored Staff Image: {request.session.get('staff_img')}")
        print(f"Stored Username: {request.session.get('staff_username')}")
        
    except Staff.DoesNotExist:
        print("Staff ID not found in database, redirecting to login...")
        return redirect("accounts:loginaccount")
    
    return redirect('staffside:pos')

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

            # ✅ Delete all cart items for this table
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


def tables(request):
    tables = Table.objects.all()

    for table in tables:
        has_orders = Cart.objects.filter(table=table).exists()
        if has_orders:
            table.status = "Occupied"
        elif table.status != "Reserved":
            table.status = "Vacant"

    context = {
        "tables": tables,
    }
    return render_page(request, 'staffside/tables.html', context)

from decimal import Decimal

def bill_page(request, table_id):
    cart_items = Cart.objects.filter(table_id=table_id)
    total_price = sum(item.price * item.quantity for item in cart_items)
    
    discount_rate = Decimal("0.10")  # Convert to Decimal
    gst_rate = Decimal("0.07")       # Convert to Decimal

    discount = total_price * discount_rate  # Ensure Decimal * Decimal
    gst = (total_price - discount) * gst_rate  # Ensure Decimal * Decimal
    final_total = (total_price - discount) + gst  # Ensure all are Decimals


    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "discount": discount,
        "gst": gst,
        "final_total": final_total,
        "table_id": table_id
    }
    return render(request, "staffside/bill_print.html", context)


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

def customer(request):
    context = {}

    if request.method == "POST":
        customer_id = request.POST.get("customer_id", "").strip()
        customer_id = int(customer_id) if customer_id.isdigit() else None

        if customer_id:  # Updating existing branch
            customer = get_object_or_404(Customer, pk=customer_id)
            form = CustomerForm(request.POST, instance=customer)  # Attach instance to show Pre-fill form with existing data and update branch
        else:  # Creating new branch
            form = CustomerForm(request.POST)

        context["form"] = form

        if form.is_valid():     #check form validation on server-side
            customer_id = request.POST.get("customer_id", "").strip()
            customer_id = int(customer_id) if customer_id.isdigit() else None
            customer_firstname = form.cleaned_data.get("customer_firstname", "").strip()
            customer_lastname = request.POST.get("customer_lastname", "").strip()
            customer_address = request.POST.get("customer_address", "").strip()
            customer_email = form.cleaned_data.get("customer_email", "").strip()
            customer_phone_no = form.cleaned_data.get("customer_phone_no", "")
            gender = request.POST.get("gender", "").strip()


            if customer_id:  # update the existing supplier data row if form data valid
                customer = form.save(commit=False)
                customer = get_object_or_404(Customer, pk=customer_id)
                customer.customer_firstname = customer_firstname
                customer.customer_lastname=customer_lastname
                customer.customer_address=customer_address
                customer.customer_email=customer_email
                customer.customer_phone_no=customer_phone_no
                customer.gender=gender
                customer.save()
                messages.success(request, "Customer updated successfully!")
            else: # add new supplier if form data valid
                Customer.objects.create(
                    customer_firstname=customer_firstname,
                    customer_lastname=customer_lastname,
                    customer_address=customer_address,
                    customer_email=customer_email,
                    customer_phone_no=customer_phone_no,
                    gender=gender
                )
                messages.success(request, "Customer added successfully!")

            return redirect("adminside:customer")

        else:
            print("Form validation failed:", form.errors)
            messages.error(request, "Form submission failed. Please correct errors.")
            context["open_form"] = True  # form open with errors

    else:
        form = CustomerForm()

    context["form"] = form
    context["customers"] = Customer.objects.all()
    return render_page(request, 'staffside/customer.html',context)
def delete_customer(request, customer_id):
    try:
        customer = get_object_or_404(Customer, pk=customer_id)

        customer.delete()  # delete customer
        return redirect("staffside:customer")  # Redirect to customer
    except Exception as e:
        return HttpResponseServerError(f"Error deleting customer: {e}")

def staffside_settings_view(request):
    return redirect('staffside:profile')

def render_settings_page(request, template, context=None):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, template, context or {})
    context = context or {}
    context["template"] = template  # Ensures `template` is still passed
    return render(request, "staffside/settings.html", context)

def change_password(request):
    form = CustomPasswordChangeForm(request.user)
    return render_settings_page(request, "staffside/settings/change_password.html", {'form': form})

def edit_profile(request):
    return render_settings_page(request,"staffside/settings/edit_profile.html")

def profile(request):
    return render_settings_page(request,"staffside/settings/profile.html")

def logout_view(request):
    return redirect('accounts:loginaccount')

