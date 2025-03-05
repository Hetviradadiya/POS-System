from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import CustomLoginForm


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


def loginaccount(request):
    form = CustomLoginForm()
    return render(request,"loginaccount.html",{'form': form})