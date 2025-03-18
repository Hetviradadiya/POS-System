from django.urls import path
from django.http import HttpResponse
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "adminside"

def empty_favicon(request):
    return HttpResponse(status=204)  # No Content

urlpatterns = [
    path('', views.home, name='home'),  
    path('dashboard/', views.dashboard, name='dashboard'),

    path('branches/', views.branches, name='branches'),
    path("branches/delete/<int:branch_id>/", views.delete_branch, name="delete_branch"),

    path('suppliers/', views.suppliers, name='suppliers'),
    path("suppliers/delete/<int:supplier_id>/", views.delete_supplier, name="delete_supplier"),

    path('purchase/', views.purchase, name='purchase'),
    path("purchase/delete/<int:purchase_id>/", views.delete_purchase, name="delete_purchase"),

    path('categories/', views.categories, name='categories'),
    # path("categories/update/<int:category_id>/", views.update_category, name="update_category"),
    path("categories/delete/<int:category_id>/", views.delete_category, name="delete_category"),

    path('inventory/', views.inventory, name='inventory'),
    path("inventory/delete/<int:inventory_id>/", views.delete_fooditem, name="delete_fooditem"),
        
    path('fooditems/', views.fooditems, name='fooditems'),
    path('tables/', views.tables, name='tables'),

    path('customer/', views.customer, name='customer'),
    path("customer/delete/<int:customer_id>/", views.delete_customer, name="delete_customer"),

    path('staff/', views.staff, name='staff'),
    path("staff/delete/<int:staff_id>/", views.delete_staff, name="delete_staff"),

    path('reports/', views.reports, name='reports'),
    path('settings/', views.adminside_settings_view, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),


    path('favicon.ico', empty_favicon),  # Handle favicon request
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
