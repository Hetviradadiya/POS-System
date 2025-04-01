from django.urls import path
from . import views
from . import pos_views

app_name = "staffside"

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.orders, name='orders'),
    path('tables/', views.tables, name='tables'),
    path('pos/', pos_views.pos, name='pos'),
    path('bill_page/<int:table_id>/',views.bill_page,name='bill_page'),
    path('sales/', views.sales, name='sales'),
    
    path('customer/', views.customer, name='customer'),
    path("customer/delete/<int:customer_id>/", views.delete_customer, name="delete_customer"),

    path('settings/', views.staffside_settings_view, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
]
