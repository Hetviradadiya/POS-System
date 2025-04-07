from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
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

def staff(request):
    context = {}

    if request.method == "POST":
        staff_id = request.POST.get("staff_id", "").strip()
        staff_id = int(staff_id) if staff_id.isdigit() else None

        if staff_id:  # Updating existing branch
            staff = get_object_or_404(Staff, pk=staff_id)
            form = StaffForm(request.POST, request.FILES, instance=staff)  # Attach instance to show Pre-fill form with existing data and update branch
        else:  # Creating new branch
            staff = None
            form = StaffForm(request.POST, request.FILES)

        context["form"] = form

        if form.is_valid():
            print("validation successfully.")
            staff_username = form.cleaned_data.get("staff_username", "").strip()
            staff_fullname = form.cleaned_data.get("staff_fullname", "").strip()
            staff_email = form.cleaned_data.get("staff_email", "").strip()
            staff_password = form.cleaned_data.get("staff_password", "").strip()  # Hashing password
            staff_phone_no = form.cleaned_data.get("staff_phone_no", "").strip()
            print("Cleaned staff_phone_no:", form.cleaned_data.get("staff_phone_no"))
            staff_role = form.cleaned_data.get("staff_role", "").strip().lower()
            branch = form.cleaned_data.get("branch", "")
            staff_img = request.FILES.get("staff_img")  # Handling image upload
            

            # print(request.POST)
            # print(request.POST.get('staff_role')) 
            if staff_id:   # update the existing branch row if form data valid
                staff = form.save(commit=False)
                staff = get_object_or_404(Staff, pk=staff_id)
                if staff_img:  # Ensure image is uploaded
                    staff.staff_img = request.FILES.get('staff_img')
                else:
                    staff.staff_img = "/staff_images/default-profile.jpg"
                staff.staff_username=staff_username
                staff.staff_fullname=staff_fullname
                staff.staff_email=staff_email
                staff.staff_password = staff_password  # The form will handle hashing
                # if staff_password:
                #     if not check_password(staff_password, staff.staff_password):  # Ensure it's not already hashed
                #         staff.staff_password = make_password(staff_password)
                # else:
                #     staff.staff_password = staff.staff_password  # Keep the existing hashed password

                staff.staff_phone_no=staff_phone_no
                staff.staff_role=staff_role
                staff.branch=branch
                staff.save()

                print("password give",staff_password)

                print("saved password",staff.staff_password)
                print("Password Match:", check_password(staff_password, staff.staff_password))

                messages.success(request, "Staff updated successfully!")

            else:# Create and save staff member
                if not staff_img:
                    staff_img = "/staff_images/default-profile.jpg"
                Staff.objects.create(
                    staff_username=staff_username,
                    staff_fullname=staff_fullname,
                    staff_email=staff_email,
                    staff_password = make_password(staff_password),
                    staff_phone_no=staff_phone_no,
                    staff_role=staff_role,
                    branch=branch,
                    staff_img = staff_img
                )
                messages.success(request, "Staff created successfully!")

            return redirect("adminside:staff")  # Redirect to staff page after successful insert

        else:
            print("Form validation failed. Errors:", form.errors) 
            messages.error(request, "Form submission failed. Please correct errors.")
            context["open_form"] = True  # form open with errors
        
    else:
        form = StaffForm()



    staff_role = request.session.get("staff_role")
    branch_id = request.session.get("branch")

    if staff_role == "manager":
        context["staff_list"] = Staff.objects.filter(branch__branch_id=branch_id)
        context["branches"] = Branch.objects.filter(branch_id=branch_id)
    else:
        context["staff_list"] = Staff.objects.all() # Fetch all staff records
        context["branches"] = Branch.objects.all()  # Get all registered branches

    return render_page(request, "adminside/staff.html", context)

def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    staff.delete()
    messages.success(request, "Staff deleted successfully.")
    return redirect("adminside:staff")

