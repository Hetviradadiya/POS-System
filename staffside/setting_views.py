from django.shortcuts import render, redirect
from django.contrib import messages
from adminside.forms import CustomPasswordChangeForm
from adminside.models import*
from adminside.forms import*
from django.utils.timezone import now


def staffside_settings_view(request):
    return redirect('staffside:profile')

def render_settings_page(request, template, context=None):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, template, context or {})
    context = context or {}
    context.update({
        "template": template,
        "today_date": now().strftime("%Y-%m-%d"),  # Current date in YYYY-MM-DD format
        "staff_username": request.session.get("staff_username", "Guest"),
    })
    return render(request, "staffside/settings.html", context)

def change_password(request):
    staff_id = request.session.get("staff_id") 
    staff = Staff.objects.get(staff_id=staff_id) 

    if request.method == "POST":
        form = CustomPasswordChangeForm(request.POST)

        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]
            confirm_password = form.cleaned_data["confirm_password"]

            # Check if old password is correct
            if not check_password(old_password, staff.staff_password):
                form.add_error("old_password", "Incorrect old password.")
                messages.error(request, "Old password is incorrect.")
            elif new_password != confirm_password:
                form.add_error("confirm_password", "New password and confirm password do not match.")
                messages.error(request, "New password and confirm password do not match.")
            else:

                staff.staff_password = new_password  # Save hashed password
                staff.save()

                print("Saved password (hashed):", staff.staff_password)
                
                # Test check_password() with the original plain-text new password
                password_match = check_password(new_password, staff.staff_password)
                print("Password Match:", password_match)

                messages.success(request, "Password updated successfully!")
                return redirect("staffside:change_password")  # Redirect after password change

    else:
        form = CustomPasswordChangeForm()
    return render_settings_page(request, "staffside/settings/change_password.html", {'form': form})

def edit_profile(request):
    staff_id = request.session.get("staff_id") 

    if request.method == "POST" and request.FILES.get("profile_pic"):
        staff = Staff.objects.get(staff_id=staff_id)

        # Get uploaded image
        image = request.FILES["profile_pic"]

        staff.staff_img = image
        staff.save()

        # Update session data
        request.session["staff_img"] = staff.staff_img.url # Full path for template use

        return redirect("staffside:edit_profile")  # Redirect after saving
    return render_settings_page(request,"staffside/settings/edit_profile.html")

def profile(request):
    return render_settings_page(request,"staffside/settings/profile.html")
