from django.urls import path
from . import views
app_name="accounts"

urlpatterns = [
#    path('logout/', views.logoutaccount,name='logoutaccount'),
   path('', views.loginaccount, name='loginaccount'),
]