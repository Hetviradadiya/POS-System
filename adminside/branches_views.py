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
        related_inventory = Inventory.objects.filter(branch=branch).exists()
        
        if related_inventory:
            return HttpResponseServerError("Cannot delete branch: Related inventory exists.")

        branch.delete()  # delete branch
        return redirect("adminside:branches")  # Redirect to branch
    except Exception as e:
        return HttpResponseServerError(f"Error deleting branch: {e}")
    