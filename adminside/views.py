from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseServerError
from .forms import CustomPasswordChangeForm
from adminside.models import*
from django.db import connection
from django.contrib import messages
from adminside.models import*
from adminside.forms import*
import re


def home(request):
    staff_id = request.session.get("staff_id")  # Get session data
    print(f"Checking session: {staff_id}")

    if not staff_id:
        print("No session found, redirecting to login...")
        return redirect("login")  # Redirect if no session found

    try:
        staff_user = Staff.objects.get(staff_id=staff_id)
        print(f"User accessing admin panel: {staff_user.staff_username}, Role: {staff_user.staff_role}")

        if staff_user.staff_role.lower() != "admin":
            print("User is not an admin, redirecting to login...")
            return redirect("login")  # Redirect non-admin users
    except Staff.DoesNotExist:
        print("Staff ID not found in database, redirecting to login...")
        return redirect("login")

    print("Rendering admin dashboard...")
    return redirect('adminside:dashboard')

def render_page(request, template, data=None):
    data=data or {}
    return render(request, "adminside/base.html", {"template": template, **data})

def dashboard(request):
    return render_page(request, 'adminside/dashboard.html')
  
def branches(request):
    context = {}

    if request.method == "POST":
        branch_id = request.POST.get("branch_id", "").strip()
        branch_id = int(branch_id) if branch_id.isdigit() else None

        if branch_id:  # Updating existing branch
            branch = get_object_or_404(Branch, pk=branch_id)
            form = BranchForm(request.POST, instance=branch)  # Attach instance to show Pre-fill form with existing data and update branch
        else:  # Creating new branch
            form = BranchForm(request.POST)

        context["form"] = form

        if form.is_valid():     #check form validation on server-side
            branch_id = request.POST.get("branch_id", "").strip()
            branch_id = int(branch_id) if branch_id.isdigit() else None
            branch_name = form.cleaned_data.get("branch_name", "").strip()
            branch_location = form.cleaned_data.get("branch_location", "").strip()
            branch_area = form.cleaned_data.get("branch_area", "").strip()
            branch_phone_no = form.cleaned_data.get("branch_phone_no", "")
            branch_status = form.cleaned_data.get("branch_status", "").strip()


            if branch_id:  # update the existing branch row if form data valid
                branch = form.save(commit=False)
                branch = get_object_or_404(Branch, pk=branch_id)
                branch.branch_name = branch_name
                branch.branch_location=branch_location
                branch.branch_area=branch_area
                branch.branch_phone_no=branch_phone_no
                branch.branch_status=branch_status
                branch.save()
                messages.success(request, "Branch updated successfully!")
            else: # create new branch if form data valid
                Branch.objects.create(
                    branch_name=branch_name,
                    branch_location=branch_location,
                    branch_area=branch_area,
                    branch_phone_no=branch_phone_no,
                    branch_status=branch_status
                )
                messages.success(request, "Branch created successfully!")

            return redirect("adminside:branches")

        else:
            print("Form validation failed:", form.errors)
            messages.error(request, "Form submission failed. Please correct errors.")
            context["open_form"] = True  # form open with errors

    else:
        form = BranchForm()

    context["form"] = form
    context["branches"] = Branch.objects.all()
    return render_page(request, "adminside/branches.html", context)

def delete_branch(request, branch_id):
    try:
        branch = get_object_or_404(Branch, pk=branch_id)

        # Check if category is linked to any inventory
        # related_inventory = Inventory.objects.filter(branch=branch).exists()
        
        # if related_inventory:
        #     return HttpResponseServerError("Cannot delete branch: Related inventory exists.")

        branch.delete()  # delete branch
        return redirect("adminside:branches")  # Redirect to branch
    except Exception as e:
        return HttpResponseServerError(f"Error deleting branch: {e}")
    
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
    

def purchase(request):    
    return render_page(request, 'adminside/purchase.html')


def categories(request):
    if request.method == "POST":
        category_id = request.POST.get("categoryId")  # Get ID 
        category_name = request.POST.get("categoryName", "").strip()
        status = request.POST.get("status") == "on"  # Convert checkbox value to Boolean

        if category_id:  # If ID exists, update category
            category = get_object_or_404(Categories, pk=category_id)
            category.categories_name = category_name
            category.status = status
            category.save()
        else:  # Create new category
            if category_name:
                Categories.objects.create(categories_name=category_name, status=status)

        return redirect("adminside:categories")  

    all_categories = Categories.objects.all()
    return render_page(request, "adminside/categories.html", {"categories": all_categories})


def update_category(request, category_id):
    category = get_object_or_404(Categories, pk=category_id)

    if request.method == "POST": 
        category_name = request.POST.get("categoryName", "").strip()
        status = request.POST.get("status") == "on" 

        if category_name:   # update data values
            category.categories_name = category_name
            category.status = status
            category.save()

        return redirect("adminside:categories")

    return render_page(request, "adminside/update_category.html", {"category": category})


def delete_category(request, category_id):
    try:
        category = get_object_or_404(Categories, pk=category_id)

        # Check if category is linked to any inventory
        related_inventory = Inventory.objects.filter(category=category).exists()
        
        if related_inventory:
            return HttpResponseServerError("Cannot delete category: Related inventory exists.")

        category.delete()  # delete category
        return redirect("adminside:categories")  # redirect to category
    except Exception as e:
        return HttpResponseServerError(f"Error deleting category: {e}")

def inventory(request):
    return render_page(request, 'adminside/inventory.html')

def fooditems(request):
    return render_page(request, 'adminside/fooditems.html')

def tables(request):
    return render_page(request, 'adminside/tables.html')

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
        customer = get_object_or_404(Supplier, pk=customer_id)

        customer.delete()  # delete supplier
        return redirect("adminside:customer")  # Redirect to supplier
    except Exception as e:
        return HttpResponseServerError(f"Error deleting customer: {e}")
    
def staff(request):
    context = {}

    if request.method == "POST":
        staff_id = request.POST.get("staff_id", "").strip()
        staff_id = int(staff_id) if staff_id.isdigit() else None

        if staff_id:  # Updating existing branch
            staff = get_object_or_404(Staff, pk=staff_id)
            form = StaffForm(request.POST, instance=staff)  # Attach instance to show Pre-fill form with existing data and update branch
        else:  # Creating new branch
            form = StaffForm(request.POST)

        context["form"] = form

        if form.is_valid():
            staff_username = form.cleaned_data.get("staff_username").strip()
            staff_fullname = form.cleaned_data.get("staff_fullname").strip()
            staff_email = form.cleaned_data.get("staff_email").strip()
            staff_password = make_password(form.cleaned_data.get("staff_password").strip())  # Hashing password
            staff_phone_no = form.cleaned_data.get("staff_phone").strip()
            staff_role = form.cleaned_data.get("staff_role").strip()
            branch = form.cleaned_data.get("branch").strip()
            staff_img = form.cleaned_data.get("staff_img")  # Handling image upload

            if staff_id:   # update the existing branch row if form data valid
                staff = form.save(commit=False)
                staff = get_object_or_404(Branch, pk=staff_id)
                staff.staff_username=staff_username,
                staff.staff_fullname=staff_fullname,
                staff.staff_email=staff_email,
                staff.staff_password=staff_password,
                staff.staff_phone_no=staff_phone_no,
                staff.staff_role=staff_role,
                staff.branch=branch,
                staff.staff_img=staff_img
                staff.save()
                messages.success(request, "Branch updated successfully!")

            else:# Create and save staff member
                Staff.objects.create(
                    staff_username=staff_username,
                    staff_fullname=staff_fullname,
                    staff_email=staff_email,
                    staff_password=staff_password,
                    staff_phone_no=staff_phone_no,
                    staff_role=staff_role,
                    branch=branch,
                    staff_img=staff_img
                )
                messages.success(request, "Branch created successfully!")

            return redirect("adminside:staff")  # Redirect to staff page after successful insert

        else:
            print("Form validation failed:", form.errors)
            messages.error(request, "Form submission failed. Please correct errors.")
            context["open_form"] = True  # form open with errors
        
    else:
        form = StaffForm()

    context["branches"] = Branch.objects.all()  # Get all registered branches
    context["staff_list"] = Staff.objects.all()  # Fetch all staff records

    return render_page(request, "adminside/staff.html", context)

def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    staff.delete()
    return redirect("staff_page")


def reports(request):
    sales_data = [
    {"product_id": "101", "product_name": "Neapolitan Pizaa", "calegories": "Pizaa", "email": "john.doe@example.com", "quentity": "450", "paid": "200", "balance": "250", "date": "01/15"},
    {"product_id": "102", "product_name": "Veg. Burger", "calegories": "Burger", "email": "jane.smith@example.com", "quentity": "350", "paid": "150", "balance": "200", "date": "01/16"},
    {"product_id": "103", "product_name": "French Fries", "calegories": "Fast Food", "email": "robert.brown@example.com", "quentity": "500", "paid": "250", "balance": "250", "date": "01/17"},
    {"product_id": "104", "product_name": "Veg. Sandvich", "calegories": "Sandvich", "email": "emily.white@example.com", "quentity": "600", "paid": "300", "balance": "300", "date": "01/18"},
    {"product_id": "105", "product_name": "Dosa (Butter)", "calegories": "South Indian", "email": "michael.green@example.com", "quentity": "750", "paid": "500", "balance": "250", "date": "01/19"},
    ]
    return render_page(request, 'adminside/reports.html', {'data':sales_data})


def adminside_settings_view(request):
    return redirect('adminside:profile')

def render_settings_page(request, template, context=None):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, template, context or {})
    context = context or {}
    context["template"] = template  # Ensures `template` is still passed
    return render(request, "adminside/settings.html", context)

def change_password(request):
    form = CustomPasswordChangeForm(request.user)
    return render_settings_page(request, "adminside/settings/change_password.html", {'form': form})

def edit_profile(request):
    return render_settings_page(request,"adminside/settings/edit_profile.html")

def profile(request):
    return render_settings_page(request,"adminside/settings/profile.html")

def logout_view(request):
    return redirect('accounts:loginaccount')







