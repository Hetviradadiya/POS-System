from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .forms import*
from adminside.models import Staff
import re
import random
from .models import PasswordResetOTP
from django.utils.crypto import get_random_string
from django.utils.timezone import now


def loginaccount(request):
    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user_input = form.cleaned_data["username"]  # Can be email or username
            password = form.cleaned_data["password"]
            print(f"Login attempt: {user_input}")

            # Determine if input is an email
            is_email = re.match(r"[^@]+@[^@]+\.[^@]+", user_input)
            
            try:
                if is_email:
                    staff_user = Staff.objects.get(staff_email=user_input)
                    print("Logging in with email")
                else:
                    staff_user = Staff.objects.get(staff_username=user_input)
                    print("Logging in with username")

                print(f"User found: {staff_user.staff_role}")

                if check_password(password, staff_user.staff_password): 
                    # login(request, Staff)

                    logout(request)
                    request.session.flush()  # Clears any previous session 
                    session_key = request.session.session_key
                    
                    request.session["staff_id"] = staff_user.staff_id  
                    request.session["staff_username"] = staff_user.staff_username  
                    request.session["staff_role"] = staff_user.staff_role 
                    
                    # request.session["staff_img"] = staff_user.staff_img
                    if staff_user.staff_img:  
                        request.session["staff_img"] = staff_user.staff_img.url  # Store image URL
                    else:
                        request.session["staff_img"] = "/staff_images/default-profile.jpg"  # Default image

                    
                    
                    if staff_user.staff_role.lower() == "admin":
                        print("Redirecting to admin dashboard")
                        return redirect("adminside:dashboard")
                    
                    elif staff_user.staff_role.lower() == "manager":
                        request.session["branch"] = staff_user.branch.branch_id
                        request.session["branch_name"] = staff_user.branch.branch_name
                        print("Redirecting to admin dashboard")
                        return redirect("adminside:dashboard")
                    
                    elif staff_user.staff_role.lower() == "staff":
                        request.session["branch"] = staff_user.branch.branch_id
                        request.session["branch_name"] = staff_user.branch.branch_name
                        print("Redirecting to POS")
                        return redirect("staffside:pos")
                    
                    else:
                        print("Unauthorized access")
                        messages.error(request, "Unauthorized access.")


                    request.session.modified = True  
                    
                    request.session.save()
                else:
                    print("Invalid password")
                    messages.error(request, "Invalid password.")

            except Staff.DoesNotExist:
                print("User does not exist")
                messages.error(request, "User does not exist.")
        
        else:
            print("Form errors:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    
    else:
        form = CustomLoginForm()
    
    return render(request, "loginaccount.html", {'form': form})


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                staff = Staff.objects.get(staff_email=email)
                otp = get_random_string(length=6, allowed_chars='0123456789')

                PasswordResetOTP.objects.create(staff=staff, otp=otp)

                send_mail(
                    'Your OTP for Password Reset',
                    f'Use this OTP to reset your password: {otp}',
                    'no-reply@example.com',
                    [email],
                    fail_silently=False,
                )
                return redirect('accounts:verify_otp', staff_id=staff.staff_id)
            except Staff.DoesNotExist:
                form.add_error('email', 'No user found with that email.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})


def generate_otp():
    return str(random.randint(100000, 999999))


def verify_otp(request, staff_id):
    try:
        staff = Staff.objects.get(staff_id=staff_id)
    except Staff.DoesNotExist:
        messages.error(request, "Invalid request.")
        return redirect('accounts:forgot_password')

    latest_otp = PasswordResetOTP.objects.filter(staff=staff).order_by('-created_at').first()

    # Handle resend OTP
    if request.method == 'POST' and 'resend' in request.POST:
        new_otp = generate_otp()
        PasswordResetOTP.objects.create(staff=staff, otp=new_otp)

        # Optional: send new OTP via email
        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP is: {new_otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[staff.staff_email],  # Assuming `staff_email` field exists
            fail_silently=True
        )

        messages.success(request, "A new OTP has been sent to your email.")
        return redirect('accounts:verify_otp', staff_id=staff_id)

    elif request.method == 'POST':
        entered_otp = ''.join([request.POST.get(f'otp{i}', '') for i in range(1, 7)])

        if not latest_otp:
            messages.error(request, "No OTP found.")
        elif latest_otp.is_expired():
            messages.error(request, "OTP has expired.")
        elif latest_otp.otp != entered_otp:
            messages.error(request, "Invalid OTP.")
        else:
            return redirect('accounts:reset_password', staff_id=staff_id)

    otp_created_at = latest_otp.created_at if latest_otp else now()
    return render(request, 'verify_otp.html', {
        'otp_created_at': otp_created_at,
    })

def reset_password(request, staff_id):
    try:
        staff = Staff.objects.get(staff_id=staff_id)
    except Staff.DoesNotExist:
        messages.error(request, "Invalid request.")
        return redirect('accounts:forgot_password')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            staff.staff_password =form.cleaned_data['new_password']
            print("staff_password",staff.staff_password)
            staff.save()
            messages.success(request, "Password reset successfully.")
            return redirect('accounts:loginaccount')
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})


    # def send_confirmation_email(user):
#     subject = "Confirmation Email"
#     message = f"Hi {user.username},\n\nYou have successfully logged in our web-site"
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [user.email]

#     try:
#         send_mail(subject, message, from_email, recipient_list)
#         print("Verification email sent successfully!")
#     except Exception as e:
#         print("Failed to send verification email:", e)

# def logoutaccount(request):        
#     logout(request)
#     return redirect('products') 

# def loginaccount(request):
#     if request.method == 'POST':
#         form = CustomLoginForm(request=request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
            
#             if user is None:
#                 messages.error(request, 'Invalid credentials. Please try again.')
#                 return render(request, 'loginaccount.html', {'form': form})
#             elif not user.is_active:
#                 messages.error(request, 'Your account is inactive. Please contact support.')
#                 return render(request, 'loginaccount.html', {'form': form})
#             else:
#                 send_confirmation_email(user) 
#                 login(request, user)
#                 messages.success(request, 'Successfully logged in!')
#                 return redirect('product_list') 
#         else:
#             messages.error(request, 'Please correct the errors below.')
#             return render(request, 'loginaccount.html', {'form': form})
    
#     else:
#         form = CustomLoginForm()
#         return render(request, 'loginaccount.html', {'form': form})