from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseServerError
from .forms import CustomPasswordChangeForm
from django.utils.timezone import now
from adminside.models import*
from adminside.forms import*

def home(request):
    staff_id = request.session.get("staff_id")  # Get session data
    print(f"Checking session: {staff_id}")

    if not staff_id:
        print("No session found, redirecting to login...")
        return redirect("accounts:loginaccount")  # Redirect if no session found

    try:
        staff_user = Staff.objects.get(staff_id=staff_id)
        print(f"User accessing admin panel: {staff_user.staff_username}, Role: {staff_user.staff_role}")

        if staff_user.staff_role.lower() != "admin":
            return redirect("accounts:loginaccount")  # Redirect non-admin users
        
    except Staff.DoesNotExist:
        print("Staff ID not found in database, redirecting to login...")
        return redirect("accounts:loginaccount")
    
    return redirect('staffside:pos')

def render_page(request, template, data=None):
    data=data or {}
    data.update({"template": template, "today_date": now().strftime("%Y-%m-%d"),"staff_username": request.session.get("staff_username", "Guest"),})
    return render(request, "staffside/base.html", data)

def orders(request):
    orders=[
        {"id":12341,"customer_name":"Kenil Patel","table":"A1","amount":200},
        {"id":12342,"customer_name":"Rasesh Patel","table":"A1","amount":1200},
        {"id":12343,"customer_name":"Brijesh Patel","table":"A1","amount":700},
        {"id":12344,"customer_name":"Shruti Patel","table":"A1","amount":500},
        {"id":12345,"customer_name":"John Patel","table":"A1","amount":900},
    ]
    return render_page(request, 'staffside/orders.html',data=orders)

def tables(request):
    return render_page(request, 'staffside/tables.html')

def pos(request):
    category_name = "All" 
    # Get staff_id from session instead of using request.user.username
    staff_id = request.session.get("staff_id")  
    if not staff_id:
        return redirect("accounts:loginaccount")  # Redirect if no session is found
    
    try:
        # Fetch staff details from session ID
        staff = Staff.objects.get(staff_id=staff_id)  
        branch = staff.branch  # Get branch of staff
        if request.method == "POST":
            category_name = request.POST.get("category","All")

        else:
            category_name == "All"
        
        if category_name == "All":
            products = Inventory.objects.filter(branch=branch)
        else:
            products = Inventory.objects.filter(category__categories_name=category_name)
        # Fetch categories and products that belong to the same branch
        categories = Categories.objects.filter(inventory__branch=branch).distinct()
        

        print(f"Staff: {staff}")
        print(f"Branch: {branch}")
        print(f"Categories: {categories}")
        print(f"Products: {products}")

        context = {
            'selectedCategory': category_name,
            'categories': categories,
            'products': products,
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

