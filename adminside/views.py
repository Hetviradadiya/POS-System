from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseServerError
from .forms import CustomPasswordChangeForm
from django.utils.timezone import now
from adminside.models import*
from django.conf import settings
from django.contrib import messages
from adminside.models import*
from adminside.forms import*
import os
import csv


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

from django.contrib.sessions.models import Session

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

from django.core.files import File

def inventory(request):
    purchase_list = Purchase.objects.all()
    branches = Branch.objects.all()
    categories = Categories.objects.all()
    food_items = Inventory.objects.all()
    form = InventoryForm()
    context = {
        "purchase_list": purchase_list,
        "branches": branches,
        "categories": categories,
        "food_items": food_items,
        "form": form,
    }

    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")

        # **CSV Upload Handling**
        if csv_file:
            try:
                decoded_file = csv_file.read().decode("utf-8").splitlines()
                reader = csv.reader(decoded_file)
                header = next(reader)  # Skip the header row
                print("CSV Header:", header)  
                normalized_header = [col.strip().lower().replace("image_name", "image") for col in header]
                required_columns = ["image","food_item", "category_id", "description", "quantity", "branch_id", "sell_price", "cost_price", "mfg_date", "exp_date"]
                
                if normalized_header != required_columns:
                    messages.error(request, "Invalid CSV format. Ensure correct columns.")
                    return redirect("adminside:inventory")

                for row in reader:
                    try:

                        image_name,food_item, category_id, description, quantity, branch_id, sell_price, cost_price, mfg_date, exp_date = row
                        category = Categories.objects.get(pk=category_id)
                        branch = Branch.objects.get(pk=branch_id)
                        # food_item = Purchase.objects.get(pk=purchase_id) if purchase_id else None

                        # **Use `form.save()` instead of `Inventory.objects.create()`**
                        inventory_form = InventoryForm(data={
                            "food_item": food_item,
                            "category": category,
                            "description": description,
                            "quantity": quantity,
                            "branch": branch,
                            "sell_price": sell_price,
                            "cost_price": cost_price,
                            "mfg_date": mfg_date,
                            "exp_date": exp_date,
                        })

                        if inventory_form.is_valid():
                            inventory = inventory_form.save(commit=False)  # Save without committing
                            image_name = row[0].strip()
                            image_path = os.path.join(settings.MEDIA_ROOT, "food_images", image_name)


                            if os.path.exists(image_path):
                                with open(image_path, "rb") as img_file:
                                    inventory.image.save(image_name, File(img_file))  # Assign image properly
                            else:
                                print(f"Image {image_name} not found at {image_path}")

                            inventory_form.save()

                        else:
                            messages.error(request, f"Invalid data in row {row}: {inventory_form.errors}")

                    except Exception as e:
                        messages.error(request, f"Error in row {row}: {str(e)}")
                        continue 

                messages.success(request, "CSV file processed successfully!")
                return redirect("adminside:inventory")

            except Exception as e:
                messages.error(request, f"Error processing CSV file: {str(e)}")
                return redirect("adminside:inventory")

        # Add manual data
        inventory_id = request.POST.get("inventory_id", "").strip()
        inventory_id = int(inventory_id) if inventory_id.isdigit() else None

        if inventory_id:
            inventory = get_object_or_404(Inventory, pk=inventory_id)
            form = InventoryForm(request.POST, request.FILES, instance=inventory)
        else:
            form = InventoryForm(request.POST, request.FILES)

        context["form"] = form

        # if form.is_valid():
        #     form.save()
        #     messages.success(request, "Inventory item saved successfully!")
        #     return redirect("adminside:inventory")
        
        #second way to store data manually

        if form.is_valid():     #check form validation on server-side
                inventory_id = request.POST.get("inventory_id", "").strip()
                inventory_id = int(inventory_id) if inventory_id.isdigit() else None
                image = request.FILES.get("image")
                food_item = form.cleaned_data.get("food_item")
                category = form.cleaned_data.get("category", "")
                description = form.cleaned_data.get("description", "").strip()
                quantity = form.cleaned_data.get("quantity", "")
                branch = form.cleaned_data.get("branch", "")
                sell_price = form.cleaned_data.get("sell_price", "")
                cost_price = form.cleaned_data.get("cost_price", "")
                mfg_date = form.cleaned_data.get("mfg_date", "")
                exp_date = form.cleaned_data.get("exp_date", "")
    

                if inventory_id:  # update the existing branch row if form data valid
                    inventory = form.save(commit=False)
                    inventory = get_object_or_404(Inventory, pk=inventory_id)
                    if image:  # Only update image if a new one is uploaded
                        inventory.image = image
                    inventory.food_item = food_item
                    inventory.category=category
                    inventory.description=description
                    inventory.quantity=quantity
                    inventory.branch=branch
                    inventory.sell_price = sell_price
                    inventory.cost_price = cost_price
                    inventory.mfg_date=mfg_date
                    inventory.exp_date=exp_date
                    inventory.save()
                    messages.success(request, "Food item updated successfully!")
                else: # create new branch if form data valid
                    Inventory.objects.create(
                        image=image,
                        food_item=food_item,
                        category=category,
                        description=description,
                        quantity=quantity,
                        branch=branch,
                        sell_price=sell_price,
                        cost_price=cost_price,
                        mfg_date=mfg_date,
                        exp_date=exp_date
                    )
                    messages.success(request, "Inventory created successfully!")

                return redirect("adminside:inventory")

        else:
            messages.error(request, "Form submission failed. Please correct errors.")
            context["open_form"] = True

    return render_page(request, "adminside/inventory.html", context)


def delete_fooditem(request, inventory_id):
    try:
        inventory = get_object_or_404(Inventory, pk=inventory_id)

        inventory.delete()  # delete fooditem
        return redirect("adminside:inventory")  # Redirect to fooditem
    except Exception as e:
        return HttpResponseServerError(f"Error deleting food-item: {e}")

def fooditems(request):
    context={}
    context['food_items'] = Inventory.objects.all()  # Fetch only stored food items from inventory
    return render_page(request, 'adminside/fooditems.html',context)

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
            form = StaffForm(request.POST, request.FILES, instance=staff)  # Attach instance to show Pre-fill form with existing data and update branch
        else:  # Creating new branch
            form = StaffForm(request.POST, request.FILES)

        context["form"] = form

        if form.is_valid():
            staff_username = form.cleaned_data.get("staff_username", "").strip()
            staff_fullname = form.cleaned_data.get("staff_fullname", "").strip()
            staff_email = form.cleaned_data.get("staff_email", "").strip()
            staff_password = make_password(form.cleaned_data.get("staff_password", "").strip())  # Hashing password
            staff_phone_no = form.cleaned_data.get("staff_phone_no", "").strip()
            print("Cleaned staff_phone_no:", form.cleaned_data.get("staff_phone_no"))
            staff_role = form.cleaned_data.get("staff_role", "").strip().lower()
            branch = form.cleaned_data.get("branch", "")
            staff_img = request.FILES.get("staff_img")  # Handling image upload
            if not staff_img:
                staff_img = "/staff_images/default-profile.jpg"

            print(request.POST)
            print(request.POST.get('staff_role')) 
            if staff_id:   # update the existing branch row if form data valid
                staff = form.save(commit=False)
                staff = get_object_or_404(Staff, pk=staff_id)
                if staff_img:  # Ensure image is uploaded
                    staff.staff_img = request.FILES['staff_img']
                staff.staff_username=staff_username
                staff.staff_fullname=staff_fullname
                staff.staff_email=staff_email
                staff.staff_password=staff_password
                staff.staff_phone_no=staff_phone_no
                staff.staff_role=staff_role
                staff.branch=branch
                staff.save()
                messages.success(request, "Staff updated successfully!")

            else:# Create and save staff member
                Staff.objects.create(
                    staff_username=staff_username,
                    staff_fullname=staff_fullname,
                    staff_email=staff_email,
                    staff_password=staff_password,
                    staff_phone_no=staff_phone_no,
                    staff_role=staff_role,
                    branch=branch,
                    staff_img = staff_img
                )
                messages.success(request, "Staff created successfully!")

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
    messages.success(request, "Staff deleted successfully.")
    return redirect("adminside:staff")


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
    logout(request)
    return redirect('accounts:loginaccount')







