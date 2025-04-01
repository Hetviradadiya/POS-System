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

def suppliers(request):
    context = {}

    if request.method == "POST":
        supplier_id = request.POST.get("supplier_id", "").strip()
        supplier_id = int(supplier_id) if supplier_id.isdigit() else None

        if supplier_id:  # Updating existing branch
            branch = get_object_or_404(Supplier, pk=supplier_id)
            form = SupplierForm(request.POST, instance=branch)  # Attach instance to show Pre-fill form with existing data and update branch
        else:  # Creating new branch
            form = SupplierForm(request.POST)

        context["form"] = form

        if form.is_valid():     #check form validation on server-side
            supplier_id = request.POST.get("supplier_id", "").strip()
            supplier_id = int(supplier_id) if supplier_id.isdigit() else None
            supplier_name = form.cleaned_data.get("supplier_name", "").strip()
            supplier_email = form.cleaned_data.get("supplier_email", "").strip()
            supplier_phone_no = form.cleaned_data.get("supplier_phone_no", "")
            company_name = form.cleaned_data.get("company_name", "").strip()
            address = form.cleaned_data.get("address", "").strip()


            if supplier_id:  # update the existing supplier data row if form data valid
                supplier = form.save(commit=False)
                supplier = get_object_or_404(Supplier, pk=supplier_id)
                supplier.supplier_name = supplier_name
                supplier.supplier_email=supplier_email
                supplier.supplier_phone_no=supplier_phone_no
                supplier.company_name=company_name
                supplier.address=address
                supplier.save()
                messages.success(request, "Supplier updated successfully!")
            else: # add new supplier if form data valid
                Supplier.objects.create(
                    supplier_name=supplier_name,
                    supplier_email=supplier_email,
                    supplier_phone_no=supplier_phone_no,
                    company_name=company_name,
                    address=address
                )
                messages.success(request, "Supplier added successfully!")

            return redirect("adminside:suppliers")

        else:
            print("Form validation failed:", form.errors)
            messages.error(request, "Form submission failed. Please correct errors.")
            context["open_form"] = True  # form open with errors

    else:
        form = SupplierForm()

    context["form"] = form
    context["suppliers"] = Supplier.objects.all()
    return render_page(request, 'adminside/suppliers.html',context)

def delete_supplier(request, supplier_id):
    try:
        supplier = get_object_or_404(Supplier, pk=supplier_id)

        supplier.delete()  # delete supplier
        return redirect("adminside:suppliers")  # Redirect to supplier
    except Exception as e:
        return HttpResponseServerError(f"Error deleting supplier: {e}")
    
