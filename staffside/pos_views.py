from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .forms import CustomPasswordChangeForm
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from adminside.models import*
from adminside.forms import*
from staffside.models import Order
from django.db.models import Sum

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

def pos(request, table_id=None):
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
        tables = Table.objects.filter(branch_id=branch)
        
        selected_table = request.POST.get("table_id") or request.GET.get("table_id")

        if selected_table:
            request.session["selected_table"] = selected_table  # Store selected table in session
            cart_items = Cart.objects.filter(table_id=selected_table , table__branch_id=branch)
        else:
            cart_items = Cart.objects.none()

        # Fetch related images
        cart_items_with_images = []
        for item in cart_items:
            purchase = Purchase.objects.filter(food_item=item.order_item).first()  # Get Purchase
            inventory = Inventory.objects.filter(food_item=purchase).first() if purchase else None  # Get Inventory
            print("inventory",inventory)
            image_url = inventory.image.url if inventory and inventory.image else None  # Get Image URL
            
            cart_items_with_images.append({
                "cart": item,
                "image_url": image_url
            })

        # Calculate total items and total price for the selected table
        total_items = cart_items.aggregate(total=Sum("quantity"))["total"] or 0
        total_price = sum(item.price * item.quantity for item in cart_items)

        if request.method == "POST":
            action = request.POST.get("action")  # Identify form action

            # **Handle Add to Cart**
            if action == "add_to_cart":
                table_id = request.POST.get("table_id")
                product_id = request.POST.get("product_id")
                size = request.POST.get("size")
                quantity = int(request.POST.get("quantity", 1))
                price = float(request.POST.get("price"))
                order_type = request.POST.get("order_type")
                customer_id = request.POST.get("customer_id") or None
                # customer = Customer.objects.get(customer_id=customer_id) if customer_id else None
                if customer_id:
                    customer_id = int(customer_id)
                

                print(f"Table ID: {table_id}, Product ID: {product_id}, Size: {size}, Quantity: {quantity}, Price: {price}")
                
                # Validation checks
                if not table_id:
                    messages.error(request, "Please select a table.")
                elif not size:
                    messages.error(request, "Please select a product size.")
                else:
                    product = get_object_or_404(Inventory, inventory_id=product_id)
                    table = get_object_or_404(Table, table_id=table_id) if table_id else None

                    # Check inventory quantity
                    if product.quantity <= 0:
                        messages.error(request, "Inventory not available for this product.")
                        return redirect(f"{reverse('staffside:pos')}?table_id={table_id}")
                    
                    cart_item, created = Cart.objects.get_or_create(
                        table=table,
                        order_item=product,
                        size= size,
                        order_type=order_type,
                        customer_id=customer_id,
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
                table_id = request.POST.get("table_id")  #  Keep the selected table

                if cart_id:
                    Cart.objects.filter(cart_id=cart_id).delete()

                # Redirect with selected table to persist selection
                messages.success(request, "Item was Deleted.")
                return redirect(f"{reverse('staffside:pos')}?table_id={table_id}")

            # **Handle Place Order**
            elif action == "place_order":
                print("Table ID for place order:", request.POST.get("table_id"))

                table_id = request.POST.get("table_id")
                customer_id = request.POST.get("customer_id")

                if not table_id:
                    messages.error(request, "Please select a table before placing an order.")
                    return redirect("staffside:pos")

                cart_items = Cart.objects.filter(table_id=table_id)

                if not cart_items.exists():
                    messages.error(request, "Cart is empty. Please add items before placing an order.")
                    return redirect("staffside:pos")

                branch_id = request.session.get("branch")
                if not branch_id:
                    return HttpResponse("No branch assigned", status=400)

                try:
                    branch_instance = Branch.objects.get(branch_id=branch_id)
                except Branch.DoesNotExist:
                    return HttpResponse("Branch not found", status=400)

                customer = None
                if customer_id:
                    try:
                        customer = Customer.objects.get(customer_id=customer_id)
                    except Customer.DoesNotExist:
                        customer = None  # Invalid ID passed

                # Check inventory availability
                insufficient_items = []

                for item in cart_items:
                    try:
                        purchase_entry = Purchase.objects.filter(
                            food_item=item.order_item,
                            branch=branch_instance
                        ).first()

                        if not purchase_entry:
                            insufficient_items.append(f"{item.order_item} (No purchase record found)")
                            continue

                        inventory_item = Inventory.objects.filter(
                            food_item_id=purchase_entry,
                            branch=branch_instance
                        ).first()

                        if item.quantity > inventory_item.quantity:
                            insufficient_items.append(
                                f"{item.order_item} (Available: {inventory_item.quantity}, Requested: {item.quantity})"
                            )
                    except Purchase.DoesNotExist:
                        insufficient_items.append(f"{item.order_item} (Not found in purchase records)")
                    except Inventory.DoesNotExist:
                        insufficient_items.append(f"{item.order_item} (Not available in inventory)")

                if insufficient_items:
                    messages.error(request, f"Order failed! Insufficient stock for: {', '.join(insufficient_items)}")
                    return redirect(f"{reverse('staffside:pos')}?table_id={table_id}")

                # All items are available, proceed with order
                total_price = sum(item.price * item.quantity for item in cart_items)
                total_quantity = sum(item.quantity for item in cart_items)

                ordered_items_str = ",".join([
                    f"{item.order_item}-{item.quantity}-{item.price * item.quantity}"
                    for item in cart_items
                ])

                existing_order = Order.objects.filter(table_id=table_id, status="pending").first()

                if existing_order:
                    existing_order.ordered_items = ordered_items_str
                    existing_order.price = total_price
                    existing_order.quantity = total_quantity
                    existing_order.customer = customer
                    existing_order.save()
                else:
                    Order.objects.create(
                        table_id=table_id,
                        ordered_items=ordered_items_str,
                        price=total_price,
                        quantity=total_quantity,
                        status="pending",
                        branch=branch_instance,
                        customer=customer 
                    )

                # Deduct quantity from Inventory
                for item in cart_items:
                    try:
                        purchase_entry = Purchase.objects.filter(
                            food_item=item.order_item,
                            branch=branch_instance
                        ).first()

                        if not purchase_entry:
                            continue  # Already handled earlier

                        inventory_item = Inventory.objects.get(
                            food_item_id=purchase_entry,
                            branch=branch_instance
                        )

                        inventory_item.quantity -= item.quantity
                        inventory_item.save()

                    except Exception as e:
                        messages.error(request, f"Error updating inventory for {item.order_item}: {e}")

                messages.success(request, "Order placed successfully.")
                return redirect("staffside:orders")

            
        # Fetch categories and products based on branch
        if category_name == "All":
            products = Inventory.objects.filter(branch=branch)
        else:
            products = Inventory.objects.filter(branch=branch, category__categories_name=category_name)
        # Fetch categories and products that belong to the same branch
        categories = Categories.objects.filter(inventory__branch=branch).distinct()
        tables = Table.objects.filter(branch_id=branch)
        customers = Customer.objects.all()
        
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
            'customers':customers,
            "cart_items": cart_items, 
            "cart_items_with_images": cart_items_with_images, 
            "selected_table": selected_table,
            "total_items": total_items,
            "total_price": total_price,
            "table_id": table_id,
        }
        
        return render_page(request, 'staffside/pos.html', context)

    except Staff.DoesNotExist:
        return redirect("accounts:loginaccount")  # Redirect if staff not found

