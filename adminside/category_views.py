from django.shortcuts import render, redirect, get_object_or_404
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
