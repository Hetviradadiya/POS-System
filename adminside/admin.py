from django.contrib import admin
from .models import Inventory,Branch,Purchase,Table,Sales_reports,Supplier,Categories,Customer,Staff

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

class StaffAdmin(admin.ModelAdmin):
    list_display=("staff_id","staff_username","staff_fullname","staff_email","staff_password","staff_phone","staff_role","branch")
admin.site.register(Staff,StaffAdmin)


class PurchaseAdmin(admin.ModelAdmin):
  list_display = ("food_item_id", "food_item", "cost_price","supplier_id","purchased_date","payment_status")
  
admin.site.register(Purchase, PurchaseAdmin)

class InventoryAdmin(admin.ModelAdmin):
  list_display = ("food_item_id", "image", "food_item_name","category","description","quantity","branch","sell_price","cost_price","mfg_date","exp_date")
  
admin.site.register(Inventory, InventoryAdmin)

# Register your models here.
admin.site.register(Table)

class SalesAdmin(admin.ModelAdmin):
    list_display=("product_id","product_name","categories","quantities")
admin.site.register(Sales_reports,SalesAdmin)

class SupplierAdmin(admin.ModelAdmin):
    list_display=("supplier_id","supplier_name","company_name","supplier_email","supplier_phone","address","branch")
admin.site.register(Supplier,SupplierAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=("categories_id","categories_name","status")
admin.site.register(Categories,CategoryAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display=("customer_id","customer_firstname","customer_lastname","customer_email","customer_phone","gender")
admin.site.register(Customer,CustomerAdmin)


