from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseServerError
from .forms import CustomPasswordChangeForm
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.conf import settings
from django.contrib import messages
from adminside.models import*
from adminside.forms import*


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
    staff_id = request.session.get("staff_id") 

    if request.method == "POST" and request.FILES.get("profile_pic"):
        staff = Staff.objects.get(staff_id=staff_id)

        # Get uploaded image
        image = request.FILES["profile_pic"]

        staff.staff_img = image
        staff.save()

        # Update session data
        request.session["staff_img"] = staff.staff_img.url # Full path for template use

        return redirect("adminside:edit_profile")  # Redirect after saving
    return render_settings_page(request,"adminside/settings/edit_profile.html")

def profile(request):
    return render_settings_page(request,"adminside/settings/profile.html")
