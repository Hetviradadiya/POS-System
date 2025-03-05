from django.urls import path
from . import views

app_name = "adminside"

urlpatterns = [
    path('', views.home, name='home'),  
    path('dashboard/', views.dashboard, name='dashboard'),
    path('branches/', views.branches, name='branches'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('purchase/', views.purchase, name='purchase'),
    path('categories/', views.categories, name='categories'),
    path('inventory/', views.inventory, name='inventory'),
    path('fooditems/', views.fooditems, name='fooditems'),
    path('tables/', views.tables, name='tables'),
    path('customer/', views.customer, name='customer'),
    path('staff/', views.staff, name='staff'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.adminside_settings_view, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
]
