from django.urls import path
from django.http import HttpResponse
from . import views,setting_views,tables_views,category_views,sales_views
from . import branches_views,suppliers_views,customer_views,staff_views,purchase_views,inventory_views
from django.conf import settings
from django.conf.urls.static import static

app_name = "adminside"

def empty_favicon(request):
    return HttpResponse(status=204)  # No Content

urlpatterns = [
    path('', views.home, name='home'),  
    path('dashboard/', views.dashboard, name='dashboard'),

    path('branches/', branches_views.branches, name='branches'),
    path("branches/delete/<int:branch_id>/", branches_views.delete_branch, name="delete_branch"),

    path('suppliers/', suppliers_views.suppliers, name='suppliers'),
    path("suppliers/delete/<int:supplier_id>/", suppliers_views.delete_supplier, name="delete_supplier"),

    path('purchase/', purchase_views.purchase, name='purchase'),
    path("purchase/delete/<int:purchase_id>/", purchase_views.delete_purchase, name="delete_purchase"),

    path('categories/', category_views.categories, name='categories'),
    path("categories/delete/<int:category_id>/", category_views.delete_category, name="delete_category"),

    path('inventory/', inventory_views.inventory, name='inventory'),
    path("inventory/delete/<int:inventory_id>/", inventory_views.delete_fooditem, name="delete_fooditem"),
        
    path('fooditems/', inventory_views.fooditems, name='fooditems'),
    path('tables/', tables_views.tables, name='tables'),

    path('customer/', customer_views.customer, name='customer'),
    path("customer/delete/<int:customer_id>/", customer_views.delete_customer, name="delete_customer"),

    path('staff/', staff_views.staff, name='staff'),
    path("staff/delete/<int:staff_id>/", staff_views.delete_staff, name="delete_staff"),

    path('reports/', sales_views.reports, name='reports'),
    path('settings/', setting_views.adminside_settings_view, name='settings'),
    path('profile/', setting_views.profile, name='profile'),
    path('edit_profile/', setting_views.edit_profile, name='edit_profile'),
    path('change_password/', setting_views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),


    path('favicon.ico', empty_favicon),  # Handle favicon request
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
