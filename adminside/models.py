from django.db import models , connection
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from adminside.models import*
from django.apps import apps

class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=50)
    branch_location = models.CharField(max_length=50)
    branch_area = models.CharField(max_length=50)
    branch_phone_no = PhoneNumberField(blank=True, null=True, error_messages={'invalid': "Enter a valid phone number (e.g., +919876543210)."})
    branch_status = models.CharField(max_length=10)
    branch_manager = models.CharField(max_length=100, blank=True, null=True)  # branch manager's name
    
    def get_manager(self):
    # """Return the assigned manager's name or 'None' if no manager is assigned."""
        manager = self.staff_members.filter(staff_role__iexact="manager").first()  # Case-insensitive check
        return manager.staff_fullname if manager else "None"

    def __str__(self):
        return f"{self.branch_id} - {self.branch_name}"
    
class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=50)
    supplier_email = models.EmailField(max_length=254)
    supplier_phone_no = PhoneNumberField(blank=True, null=True, error_messages={'invalid': "Enter a valid phone number (e.g., +919876543210)."})
    company_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.supplier_id} - {self.supplier_name}"

class Categories(models.Model):
    categories_id = models.AutoField(primary_key=True)
    categories_name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.categories_id} - {self.categories_name}"
    
class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    food_item = models.CharField(max_length=50)
    quantity = models.IntegerField(null=True, blank=True)
    cost_price = models.IntegerField(null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, db_column="supplier_id",null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column="branch_id",null=True, blank=True)
    purchased_date = models.DateField()
    payment_status = models.CharField(max_length=10)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     # Check if the food item already exists in inventory
    #     inventory_item, created = Inventory.objects.get_or_create(
    #         food_item=self,
    #         defaults={
    #             "category": None,  # Set category later if needed
    #             "quantity": 0,
    #             "branch": self.supplier.branch,
    #             "cost_price": self.cost_price,
    #         }
    #     )

    #     if not created:
    #         inventory_item.quantity += 1  # Update quantity if already exists
    #         inventory_item.save()

    def __str__(self):
        return f"{self.purchase_id} - {self.food_item}"

class Staff(models.Model):

    staff_id = models.AutoField(primary_key=True)
    staff_username = models.CharField(max_length=50, unique=True)
    staff_fullname = models.CharField(max_length=100)
    staff_email = models.EmailField(max_length=50, unique=True)
    staff_password = models.CharField(max_length=128)
    staff_phone_no = PhoneNumberField(blank=True, null=True, error_messages={'invalid': "Enter a valid phone number (e.g., +919876543210)."})
    staff_img = models.ImageField(upload_to='staff_images/', default='staff_images/default-profile.jpg', null=True, blank=True)
    staff_role = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, db_column="branch_id", related_name="staff_members")
    session_keys = models.JSONField(default=list)  # Store multiple session keys

    def save(self, *args, **kwargs):
        if self.pk:  # If updating an existing user
            existing_staff = Staff.objects.filter(pk=self.pk).first()
            if existing_staff and existing_staff.staff_password != self.staff_password:
                self.staff_password = make_password(self.staff_password)
        else:  # If creating a new user
            if not self.staff_password.startswith("pbkdf2_sha256$"):
                self.staff_password = make_password(self.staff_password)

        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.staff_password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Verifies the entered password against the hashed password."""
        if not self.staff_password:
            return False  # Prevent errors when password is None
        return check_password(raw_password, self.staff_password)

    def __str__(self):
        return f"{self.staff_fullname}-{self.staff_role}"

class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='food_images/', blank=True, null= True)
    food_item = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True, blank=True, db_column="food_item_id")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, db_column="categories_id")
    description = models.TextField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column="branch_id")
    sell_price = models.IntegerField(null=True, blank=True)
    cost_price = models.IntegerField(null=True, blank=True)
    mfg_date = models.DateField(null=True, blank=True)
    exp_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.food_item.food_item if self.food_item else 'No Food Item'}"

class Table(models.Model):
    STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
    ]

    table_id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="tables", null=True, blank=True, db_column="branch_id")
    table_number = models.CharField(max_length=10, blank=True, null=True)  # Store 'T-1', 'T-2'
    seats = models.IntegerField(null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='vacant')

    class Meta:
        unique_together = ("branch", "table_number")

    def save(self, *args, **kwargs):
        """Auto-generate table_number based on branch."""
        if not self.table_number:
            last_table = Table.objects.filter(branch=self.branch).order_by("-table_id").first()
            next_number = 1

            if last_table and last_table.table_number:
                last_table_number = str(last_table.table_number)  # Ensure it's a string
                if "-" in last_table_number:
                    try:
                        next_number = int(last_table_number.split("-")[1]) + 1
                    except (IndexError, ValueError):
                        next_number = 1  # Fallback in case of parsing error

            self.table_number = f"T-{next_number}"  # Format table number per branch

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Table {self.table_number} ({self.branch.branch_name}) - {self.status}"
    


    # def save(self, *args, **kwargs):
    #     """Auto-generate table_number if not provided."""
    #     if not self.table_number:
    #         last_table = Table.objects.order_by("-table_id").first()
    #         next_number = 1

    #     if last_table and last_table.table_number:
    #         last_table_number = str(last_table.table_number)  # Ensure it's a string
    #         if "-" in last_table_number:  # Prevents AttributeError
    #             try:
    #                 next_number = int(last_table_number.split("-")[1]) + 1
    #             except (IndexError, ValueError):
    #                 next_number = 1  # Fallback in case of parsing error

    #     self.table_number = f"T-{next_number}"

    #     """Override save to clear cart when status is changed to vacant."""
    #     super().save(*args, **kwargs)
    #     # if self.status == 'vacant':
    #     #     Cart.objects.filter(table=self).delete()  # Clear cart when table becomes vacant

    # def __str__(self):
    #     return f"Table {self.table_id} - {self.status}"

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, db_column="table_id")
    order_item = models.CharField(max_length=255)
    size = models.CharField(max_length=20, choices=[("Small", "Small"), ("Medium", "Medium"), ("Large", "Large")], default="Medium")
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Cart {self.cart_id} - Table {self.table.table_id}"

class Customer(models.Model):
  customer_id = models.AutoField(primary_key=True) 
  customer_firstname = models.CharField(max_length=50)
  customer_lastname = models.CharField(max_length=50,blank=True, null=True)
  customer_address = models.CharField(max_length=255,blank=True, null=True)
  customer_email=models.EmailField(max_length=50,unique=True)
  customer_phone_no=PhoneNumberField(blank=True, null=True, error_messages={'invalid': "Enter a valid phone number (e.g., +919876543210)."})
  gender=models.CharField(max_length=50)


class SalesReport(models.Model):
    sales_id = models.AutoField(primary_key=True)
    order = models.ForeignKey("staffside.Order", on_delete=models.CASCADE, db_column="order_id", null=True, blank=True)  # Link to Order
    quantity_sold = models.IntegerField()
    branch =  models.ForeignKey(Branch, on_delete=models.CASCADE,db_column="branch_id", null=True, blank=True)
    customer = models.CharField(max_length=255, null=True, blank=True)
    staff = models.CharField(max_length=255, null=True, blank=True)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sales_id} - {self.quantity_sold} sold at {self.branch}"
