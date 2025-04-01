from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseServerError
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib import messages
from adminside.models import*
from adminside.forms import*

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

def purchase(request):  
    context = {}

    if request.method == "POST":
        purchase_id = request.POST.get("purchase_id", "").strip()
        purchase_id = int(purchase_id) if purchase_id.isdigit() else None

        if purchase_id:  # Updating existing branch
            purchase = get_object_or_404(Purchase, pk=purchase_id)
            form = PurchaseForm(request.POST, instance=purchase)  # Attach instance to show Pre-fill form with existing data and update branch
        else:  # Creating new branch
            form = PurchaseForm(request.POST)

        context["form"] = form

        if form.is_valid():     #check form validation on server-side
            purchase_id = request.POST.get("purchase_id", "").strip()
            purchase_id = int(purchase_id) if purchase_id.isdigit() else None
            food_item = form.cleaned_data.get("food_item", "").strip()
            quantity = form.cleaned_data.get("quantity", "")
            cost_price = form.cleaned_data.get("cost_price", "")
            branch = form.cleaned_data.get("branch", "")
            supplier = form.cleaned_data.get("supplier", "")
            purchased_date = form.cleaned_data.get("purchased_date", "")
            payment_status = form.cleaned_data.get("payment_status", "").strip()


            if purchase_id:  # update the existing branch row if form data valid
                purchase = form.save(commit=False)
                purchase = get_object_or_404(Purchase, pk=purchase_id)
                purchase.food_item = food_item
                purchase.quantity=quantity
                purchase.cost_price = cost_price
                purchase.branch=branch
                purchase.supplier=supplier
                purchase.purchased_date=purchased_date
                purchase.payment_status=payment_status
                purchase.save()
                messages.success(request, "Details updated successfully!")
            else: # create new branch if form data valid
                Purchase.objects.create(
                    food_item=food_item,
                    quantity=quantity,
                    cost_price=cost_price,
                    branch=branch,
                    supplier=supplier,
                    purchased_date=purchased_date,
                    payment_status=payment_status
                )
                messages.success(request, "purchase created successfully!")

            return redirect("adminside:purchase")

        else:
            print("Form validation failed:", form.errors)
            messages.error(request, "Form submission failed. Please correct errors.")
            context["open_form"] = True  # form open with errors

    else:
        form = PurchaseForm()

    context["form"] = form
    context["branches"] = Branch.objects.all() 
    context["suppliers"] = Supplier.objects.all()
    context["purchase_list"] = Purchase.objects.all() 
    return render_page(request, 'adminside/purchase.html',context)

def delete_purchase(request, purchase_id):
    try:
        purchase = get_object_or_404(Purchase, pk=purchase_id)

        # Check if purchase is linked to any inventory
        related_inventory = Inventory.objects.filter(purchase=purchase).exists()
        
        if related_inventory:
            return HttpResponseServerError("Cannot delete purchase: Related inventory exists.")

        purchase.delete()  # delete branch
        return redirect("adminside:purchase")  # Redirect to branch
    except Exception as e:
        return HttpResponseServerError(f"Error deleting purchase: {e}")
    