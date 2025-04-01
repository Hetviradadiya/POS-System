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
    return render_page(request, 'adminside/customer.html',context)

def delete_customer(request, customer_id):
    try:
        customer = get_object_or_404(Customer, pk=customer_id)

        customer.delete()  # delete customer
        return redirect("adminside:customer")  # Redirect to customer
    except Exception as e:
        return HttpResponseServerError(f"Error deleting customer: {e}")
    