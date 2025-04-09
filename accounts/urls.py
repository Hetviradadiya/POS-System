from django.urls import path
from . import views
app_name="accounts"

urlpatterns = [
#    path('logout/', views.logoutaccount,name='logoutaccount'),
   path('', views.loginaccount, name='loginaccount'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/<int:staff_id>/', views.verify_otp, name='verify_otp'),
    path('reset-password/<int:staff_id>/', views.reset_password, name='reset_password'),
]