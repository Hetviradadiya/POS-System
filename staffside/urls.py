from django.urls import path
from . import views
from . import pos_views,order_views,sales_views,customer_views,tables_views,setting_views

app_name = "staffside"

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', order_views.orders, name='orders'),
    path('tables/', tables_views.tables, name='tables'),
    path('pos/', pos_views.pos, name='pos'),
    path('bill_page/<int:table_id>/',views.bill_page,name='bill_page'),
    path('sales/', sales_views.sales, name='sales'),
    
    path('customer/', customer_views.customer, name='customer'),
    path("customer/delete/<int:customer_id>/", customer_views.delete_customer, name="delete_customer"),

    path('settings/', setting_views.staffside_settings_view, name='settings'),
    path('profile/', setting_views.profile, name='profile'),
    path('edit_profile/', setting_views.edit_profile, name='edit_profile'),
    path('change_password/', setting_views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
]
