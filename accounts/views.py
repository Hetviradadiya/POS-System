from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
# from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .forms import CustomLoginForm
from adminside.models import Staff


def loginaccount(request):
    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]  
            password = form.cleaned_data["password"]
            print(f"Login attempt: {username}")

            try:
                staff_user = Staff.objects.get(staff_username=username)
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