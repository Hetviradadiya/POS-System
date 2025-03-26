from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseServerError
from .forms import CustomPasswordChangeForm
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from adminside.models import*
from adminside.forms import*
from staffside.models import Order
from django.db.models import Sum

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
    orders_by_table = {}  # Store cart items grouped by table
    tables = Table.objects.all()
    for table in tables:
        cart_items = Cart.objects.filter(table=table)  # Get cart items for this table
        if cart_items.exists():
            orders_by_table[table.table_id] = cart_items  # Store items in dictionary
    context = {
        'orders_by_table': orders_by_table
    }

    return render_page(request, 'staffside/orders.html',context)

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

def pos(request):
    category_name = request.POST.get("category", "All") 
    # print(f"Selected Category: {category_name}") 
    # Get staff_id from session instead of using request.user.username
    staff_id = request.session.get("staff_id")  
    if not staff_id:
        return redirect("accounts:loginaccount")  # Redirect if no session is found
    
    try:
        # Fetch staff details from session ID
        staff = Staff.objects.get(staff_id=staff_id)  
        branch = staff.branch  # Get branch of staff
        tables = Table.objects.all()
        
        selected_table = request.POST.get("table_id") or request.GET.get("table_id") or request.session.get("selected_table")

        if selected_table:
            request.session["selected_table"] = selected_table  # Store selected table in session
            cart_items = Cart.objects.filter(table_id=selected_table)
        else:
            cart_items = Cart.objects.none()

        # ✅ **Calculate total items and total price for the selected table**
        total_items = cart_items.aggregate(total=Sum("quantity"))["total"] or 0
        total_price = sum(item.price * item.quantity for item in cart_items)

        if request.method == "POST":
            action = request.POST.get("action")  # Identify form action

            # **Handle Add to Cart**
            if action == "add_to_cart":
                order_type = request.POST.get("order_type")
                table_id = request.POST.get("table_id")
                product_id = request.POST.get("product_id")
                size = request.POST.get("size")
                quantity = int(request.POST.get("quantity", 1))
                price = float(request.POST.get("price"))

                print(f"Table ID: {table_id}, Product ID: {product_id}, Size: {size}, Quantity: {quantity}, Price: {price}")
                
                # Validation checks
                if not table_id:
                    messages.error(request, "Please select a table.")
                elif not size:
                    messages.error(request, "Please select a product size.")
                else:
                    product = get_object_or_404(Inventory, inventory_id=product_id)
                    table = get_object_or_404(Table, table_id=table_id) if table_id else None

                    # Cart.objects.create(
                    #     table=table,
                    #     order_item=product,
                    #     size=size,
                    #     quantity=quantity,
                    #     price=price,
                    # )
                    cart_item, created = Cart.objects.get_or_create(
                        table=table,
                        order_item=product,
                        size= size,
                        defaults={ "quantity": quantity, "price": price}
                    )
                    if not created:
                        cart_item.quantity += quantity
                        cart_item.save()
                    messages.success(request, "Item added to cart successfully.")
                
                return redirect(f"{reverse('staffside:pos')}?table_id={table_id}")
            
            elif action == "update_quantity":
                cart_id = request.POST.get("cart_id")
                table_id = request.POST.get("table_id")
                change = int(request.POST.get("change"))  # Get the +1 or -1 value
                # new_quantity = int(request.POST.get("quantity"))

                # Find the cart item
                cart_item = get_object_or_404(Cart, cart_id=cart_id)
                cart_item.quantity += change  # Increase or decrease quantity
                if cart_item.quantity < 1:
                    cart_item.quantity = 1  # Prevent negative quantity
                cart_item.save()

                messages.success(request, "Item updated successfully.")
                
                return redirect(f"{reverse('staffside:pos')}?table_id={table_id}")
            
            elif action == "remove_from_cart":
                cart_id = request.POST.get("cart_id")
                table_id = request.POST.get("table_id")  # ✅ Keep the selected table

                if cart_id:
                    Cart.objects.filter(cart_id=cart_id).delete()

                # Redirect with selected table to persist selection
                messages.success(request, "Item was Deleted.")
                return redirect(f"{reverse('staffside:pos')}?table_id={table_id}")

            # **Handle Place Order**
            elif action == "place_order":
                # order_type = request.POST.get("order_type")
                table_id = request.POST.get("table_id") 

                if not table_id:
                    messages.error(request, "Please select a table before placing an order.")
                    return redirect("staffside:pos")

                cart_items = Cart.objects.filter(table_id=table_id)  # Get cart items only for the selected table

                if not cart_items.exists():
                    messages.error(request, "Cart is empty. Please add items before placing an order.")
                    return redirect("staffside:pos")

                total_price = sum(item.price * item.quantity for item in cart_items)
                total_quantity = sum(item.quantity for item in cart_items)

                # Save order without deleting cart
                order = Order.objects.create(
                    table_id=table_id,
                    ordered_items=[
                        {"product": item.order_item.id, "size": item.size, "quantity": item.quantity}
                        for item in cart_items
                    ],
                    price=total_price,
                    quantity=total_quantity,
                    status="pending",
                    order_type=order_type,
                )

                messages.success(request, "Order placed successfully.")
                return redirect("staffside:orders")

            
        # Fetch categories and products based on branch
        if category_name == "All":
            products = Inventory.objects.filter(branch=branch)
        else:
            products = Inventory.objects.filter(branch=branch, category__categories_name=category_name)
        # Fetch categories and products that belong to the same branch
        categories = Categories.objects.filter(inventory__branch=branch).distinct()
        tables = Table.objects.all()
        
        # print(f"Staff: {staff}")
        # print(f"Branch: {branch}")
        # print(f"Categories: {categories}")
        # print(f"Products: {products}")
        # print(f"Tables: {tables}")
        # print(f"cart_items :{cart_items}")

        context = {
            'selectedCategory': category_name,
            'categories': categories,
            'products': products,
            'tables': tables,
            "cart_items": cart_items, 
            "selected_table": selected_table,
            "total_items": total_items,
            "total_price": total_price,
        }
        
        return render_page(request, 'staffside/pos.html', context)

    except Staff.DoesNotExist:
        return redirect("accounts:loginaccount")  # Redirect if staff not found

def sales(request):
    return render_page(request, 'staffside/sales.html')

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

