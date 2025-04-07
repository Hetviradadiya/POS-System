from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseServerError
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.conf import settings
from django.contrib import messages
from adminside.models import*
from adminside.forms import*
import os
import csv
from django.core.files import File

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

# def inventory(request):
#     purchase_list = Purchase.objects.all()
#     branches = Branch.objects.all()
#     categories = Categories.objects.all()
#     food_items = Inventory.objects.all()
#     form = InventoryForm()
#     context = {
#         "purchase_list": purchase_list,
#         "branches": branches,
#         "categories": categories,
#         "food_items": food_items,
#         "form": form,
#     }

#     if request.method == "POST":
#         print("POST Data:", request.POST)

#         csv_file = request.FILES.get("csv_file")
#         print("FILES:", request.FILES)

#         # **CSV Upload Handling**
#         if csv_file:
#             try:
#                 decoded_file = csv_file.read().decode("utf-8-sig").splitlines()
#                 reader = csv.reader(decoded_file)
#                 header = next(reader)  # Skip the header row
#                 print("CSV Header:", header)  
#                 normalized_header = [col.strip().lower().replace("image_name", "image") for col in header]
#                 required_columns = ["image","food_item", "category_id", "description", "quantity", "branch_id", "sell_price", "cost_price", "mfg_date", "exp_date"]
                
#                 if normalized_header != required_columns:
#                     messages.error(request, "Invalid CSV format. Ensure correct columns.")
#                     return redirect("adminside:inventory")

#                 for row in reader:
#                     try:

#                         image_name,food_item, category_id, description, quantity, branch_id, sell_price, cost_price, mfg_date, exp_date = row
#                         category = Categories.objects.get(pk=category_id)
#                         branch = Branch.objects.get(pk=branch_id)
#                         # food_item = Purchase.objects.get(pk=purchase_id) if purchase_id else None

#                         # **Use `form.save()` instead of `Inventory.objects.create()`**
#                         inventory_form = InventoryForm(data={
#                             "food_item": food_item,
#                             "category": category,
#                             "description": description,
#                             "quantity": quantity,
#                             "branch": branch,
#                             "sell_price": sell_price,
#                             "cost_price": cost_price,
#                             "mfg_date": mfg_date,
#                             "exp_date": exp_date,
#                         })

#                         if inventory_form.is_valid():
#                             inventory = inventory_form.save(commit=False)  # Save without committing
#                             image_name = row[0].strip()
#                             image_path = os.path.join(settings.MEDIA_ROOT, "food_images", image_name)


#                             if os.path.exists(image_path):
#                                 with open(image_path, "rb") as img_file:
#                                     inventory.image.save(image_name, File(img_file))  # Assign image
#                             else:
#                                 print(f"Image {image_name} not found at {image_path}")
#                                 messages.error(request, f"Image {image_name} not found at {image_path}, skipping row.")
#                                 continue 
#                             inventory_form.save()

#                         else:
#                             messages.error(request, f"Invalid data in row {row}: {inventory_form.errors}")

#                     except Exception as e:
#                         messages.error(request, f"Error in row {row}: {str(e)}")
#                         continue 

#                 messages.success(request, "CSV file processed successfully!")
#                 return redirect("adminside:inventory")

#             except Exception as e:
#                 messages.error(request, f"Error processing CSV file: {str(e)}")
#                 return redirect("adminside:inventory")

#         # Add manual data
#         inventory_id = request.POST.get("inventory_id", "").strip()
#         inventory_id = int(inventory_id) if inventory_id.isdigit() else None

#         if inventory_id:
#             inventory = get_object_or_404(Inventory, pk=inventory_id)
#             form = InventoryForm(request.POST, request.FILES, instance=inventory)
#         else:
#             form = InventoryForm(request.POST, request.FILES)

#         context["form"] = form

#         if form.is_valid():
#             instance = form.save()
#             print("Saved Inventory:", instance.pk)
#             messages.success(request, "Inventory item saved successfully!")
#             return redirect("adminside:inventory")
        
#         #second way to store data manually

#         # if form.is_valid():     #check form validation on server-side
#         #         inventory_id = request.POST.get("inventory_id", "").strip()
#         #         inventory_id = int(inventory_id) if inventory_id.isdigit() else None
#         #         image = request.FILES.get("image")
#         #         food_item = form.cleaned_data.get("food_item")
#         #         category = form.cleaned_data.get("category", "")
#         #         description = form.cleaned_data.get("description", "").strip()
#         #         quantity = form.cleaned_data.get("quantity", "")
#         #         branch = form.cleaned_data.get("branch", "")
#         #         sell_price = form.cleaned_data.get("sell_price", "")
#         #         cost_price = form.cleaned_data.get("cost_price", "")
#         #         mfg_date = form.cleaned_data.get("mfg_date", "")
#         #         exp_date = form.cleaned_data.get("exp_date", "")
    

#         #         if inventory_id:  # update the existing branch row if form data valid
#         #             inventory = form.save(commit=False)
#         #             inventory = get_object_or_404(Inventory, pk=inventory_id)
#         #             if image:  # Only update image if a new one is uploaded
#         #                 inventory.image = image
#         #             inventory.food_item = food_item
#         #             inventory.category=category
#         #             inventory.description=description
#         #             inventory.quantity=quantity
#         #             inventory.branch=branch
#         #             inventory.sell_price = sell_price
#         #             inventory.cost_price = cost_price
#         #             inventory.mfg_date=mfg_date
#         #             inventory.exp_date=exp_date
#         #             inventory.save()
#         #             messages.success(request, "Food item updated successfully!")
#         #         else: # create new branch if form data valid
#         #             Inventory.objects.create(
#         #                 image=image,
#         #                 food_item=food_item,
#         #                 category=category,
#         #                 description=description,
#         #                 quantity=quantity,
#         #                 branch=branch,
#         #                 sell_price=sell_price,
#         #                 cost_price=cost_price,
#         #                 mfg_date=mfg_date,
#         #                 exp_date=exp_date
#         #             )
#         #             messages.success(request, "Inventory created successfully!")

#         #         return redirect("adminside:inventory")

#         else:
#             if not form.is_valid():
#                 print("form error:",form.errors)
#                 messages.error(request, "Form submission failed. Please correct errors.")
#             context["open_form"] = True

#     return render_page(request, "adminside/inventory.html", context)


def inventory(request):
    staff_role = request.session.get("staff_role")
    branch_id = request.session.get("branch")  # From session
    
    # Filter data based on manager's branch
    if staff_role == "manager":
        purchase_list = Purchase.objects.filter(branch__branch_id=branch_id)
        branches = Branch.objects.filter(branch_id=branch_id)
        food_items = Inventory.objects.filter(branch__branch_id=branch_id)
    else:
        purchase_list = Purchase.objects.all()
        branches = Branch.objects.all()
        food_items = Inventory.objects.all()


    categories = Categories.objects.all()
    form = InventoryForm()

    context = {
        "purchase_list": purchase_list,
        "branches": branches,
        "categories": categories,
        "food_items": food_items,
        "form": form,
        "open_form": False,  # Keeps form open
    }

    if request.method == "POST":
        print("POST Data:", request.POST)

        purchase_id = request.POST.get("purchase_id")
        if purchase_id:
            try:
                purchase = get_object_or_404(Purchase, pk=purchase_id)
                initial_data = {
                    "food_item": purchase.food_item,  # Assuming Purchase has a food_item field
                    "quantity": purchase.quantity,
                    "branch": purchase.branch,
                    "cost_price": purchase.cost_price,
                    "mfg_date": purchase.purchased_date,
                }
                form = InventoryForm(initial=initial_data)
                context["form"] = form
                context["open_form"] = True  # Keeps form open
                # return render_page(request, "adminside/inventory.html", context)
            except Exception as e:
                messages.error(request, f"Error fetching purchase data: {str(e)}")

        # **CSV Upload Handling**
        csv_file = request.FILES.get("csv_file")
        if csv_file:
            try:
                decoded_file = csv_file.read().decode("utf-8-sig").splitlines()
                reader = csv.reader(decoded_file)
                header = next(reader)
                print("CSV Header:", header) 
                normalized_header = [col.strip().lower().replace("image_name", "image") for col in header]
                required_columns = ["image", "food_item", "category_id", "description", "quantity", "branch_id", "sell_price", "cost_price", "mfg_date", "exp_date"]

                if normalized_header != required_columns:
                    messages.error(request, "Invalid CSV format. Ensure correct columns.")
                    return redirect("adminside:inventory")

                for row in reader:
                    try:
                        image_name, food_item, category_id, description, quantity, branch_id, sell_price, cost_price, mfg_date, exp_date = row
                        category = Categories.objects.get(pk=category_id)
                        branch = Branch.objects.get(pk=branch_id)
                        # food_item = Purchase.objects.get(pk=purchase_id) if purchase_id else None

                        inventory_form = InventoryForm(data={
                            "food_item": food_item,
                            "category": category.categories_id,
                            "description": description,
                            "quantity": quantity,
                            "branch": branch.branch_id,
                            "sell_price": sell_price,
                            "cost_price": cost_price,
                            "mfg_date": mfg_date,
                            "exp_date": exp_date,
                        })

                        if inventory_form.is_valid():
                            inventory = inventory_form.save(commit=False)
                            image_name = row[0].strip()
                            image_path = os.path.join(settings.MEDIA_ROOT, "food_images", image_name)

                            if os.path.exists(image_path):
                                with open(image_path, "rb") as img_file:
                                    inventory.image.save(image_name, File(img_file))  # Assign image
                            else:
                                print(f"Image {image_name} not found at {image_path}")
                                messages.error(request, f"Image {image_name} not found at {image_path}, skipping row.")
                                continue 

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

        # Manual Form Submission
        
        inventory_id = request.POST.get("inventory_id", "").strip()
        inventory_id = int(inventory_id) if inventory_id.isdigit() else None

        if inventory_id:
            inventory = get_object_or_404(Inventory, pk=inventory_id)
            form = InventoryForm(request.POST, request.FILES, instance=inventory)
        else:
            form = InventoryForm(request.POST, request.FILES)

        context["form"] = form
        # context["open_form"] = True  # Keep form open

        if form.is_valid():
            instance = form.save()
            print("Saved Inventory:", instance.pk)
            messages.success(request, "Inventory item saved successfully!")
            return redirect("adminside:inventory")
        
        #second way to store data manually

        # if form.is_valid():     #check form validation on server-side
        #         inventory_id = request.POST.get("inventory_id", "").strip()
        #         inventory_id = int(inventory_id) if inventory_id.isdigit() else None
        #         image = request.FILES.get("image")
        #         food_item = form.cleaned_data.get("food_item")
        #         category = form.cleaned_data.get("category", "")
        #         description = form.cleaned_data.get("description", "").strip()
        #         quantity = form.cleaned_data.get("quantity", "")
        #         branch = form.cleaned_data.get("branch", "")
        #         sell_price = form.cleaned_data.get("sell_price", "")
        #         cost_price = form.cleaned_data.get("cost_price", "")
        #         mfg_date = form.cleaned_data.get("mfg_date", "")
        #         exp_date = form.cleaned_data.get("exp_date", "")
    

        #         if inventory_id:  # update the existing branch row if form data valid
        #             inventory = form.save(commit=False)
        #             inventory = get_object_or_404(Inventory, pk=inventory_id)
        #             if image:  # Only update image if a new one is uploaded
        #                 inventory.image = image
        #             inventory.food_item = food_item
        #             inventory.category=category
        #             inventory.description=description
        #             inventory.quantity=quantity
        #             inventory.branch=branch
        #             inventory.sell_price = sell_price
        #             inventory.cost_price = cost_price
        #             inventory.mfg_date=mfg_date
        #             inventory.exp_date=exp_date
        #             inventory.save()
        #             messages.success(request, "Food item updated successfully!")
        #         else: # create new branch if form data valid
        #             Inventory.objects.create(
        #                 image=image,
        #                 food_item=food_item,
        #                 category=category,
        #                 description=description,
        #                 quantity=quantity,
        #                 branch=branch,
        #                 sell_price=sell_price,
        #                 cost_price=cost_price,
        #                 mfg_date=mfg_date,
        #                 exp_date=exp_date
        #             )
        #             messages.success(request, "Inventory created successfully!")

        #         return redirect("adminside:inventory")

        else:
            if not form.is_valid():
                print("Form Errors:", form.errors)  # This will show errors in the terminal
                messages.error(request, f"Form submission failed: {form.errors}")
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
    staff_role = request.session.get("staff_role")
    branch_id = request.session.get("branch")

    if staff_role == "manager":
        food_items = Inventory.objects.filter(branch__branch_id=branch_id)
    else:
        food_items = Inventory.objects.all()

    context = {
        "food_items": food_items
    }
    return render_page(request, 'adminside/fooditems.html',context)
