from django.contrib import admin
from .models import Inventory,Branch,Purchase,Table,SalesReport,Supplier,Categories,Customer,Staff

# Register your models here.
# @admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
  list_display = ("branch_id", "branch_location", "branch_area","branch_phone_no","branch_status","get_manager")
  
  def get_manager(self, obj):
    # """Retrieve the manager's name for the branch or return 'None' if no manager is assigned."""
    manager = obj.staff_members.filter(staff_role="Manager").first()
    return manager.staff_fullname if manager else "None"

  get_manager.short_description = "Branch Manager"
  
admin.site.register(Branch, BranchAdmin)


class SupplierAdmin(admin.ModelAdmin):
    list_display=("supplier_id","supplier_name","company_name","supplier_email","supplier_phone_no","address")
admin.site.register(Supplier,SupplierAdmin)

class StaffAdmin(admin.ModelAdmin):
    list_display=("staff_id","staff_username","staff_fullname","staff_email","staff_password","staff_phone_no","staff_role","branch")
admin.site.register(Staff,StaffAdmin)


class CategoryAdmin(admin.ModelAdmin):
  list_display=("categories_id","categories_name","status")
admin.site.register(Categories,CategoryAdmin)

class InventoryAdmin(admin.ModelAdmin):
  list_display = ("inventory_id","food_item","category","description","quantity","branch","image","sell_price","cost_price","mfg_date","exp_date")
  
admin.site.register(Inventory, InventoryAdmin)

class PurchaseAdmin(admin.ModelAdmin):
  list_display = ("purchase_id", "food_item","quantity", "cost_price","branch","supplier","purchased_date","payment_status")
  
admin.site.register(Purchase, PurchaseAdmin)


# Register your models here.
admin.site.register(Table)


class CustomerAdmin(admin.ModelAdmin):
    list_display=("customer_id","customer_firstname","customer_lastname","customer_email","customer_phone_no","gender")
admin.site.register(Customer,CustomerAdmin)

class SalesAdmin(admin.ModelAdmin):
    list_display=("sales_id", "product", "category", "quantity_sold", "branch", "supplier", "customer", "staff", "sale_date")
admin.site.register(SalesReport,SalesAdmin)


