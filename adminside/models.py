
from django.db import models , connection
from phonenumber_field.modelfields import PhoneNumberField

class Branch(models.Model):
    id=models.AutoField(primary_key=True)
    location=models.CharField(max_length=50)
    area=models.CharField(max_length=50)
    manager_id=models.IntegerField(null=False)
    phone_no=PhoneNumberField()
    status=models.CharField(max_length=10)

class Purchase(models.Model):
    food_item_id=models.AutoField(primary_key=True)
    food_item=models.CharField(max_length=50)
    cost_price=models.IntegerField(null=False)
    supplier_id=models.IntegerField(null=False)
    purchased_date=models.DateField()
    payment_status=models.CharField(max_length=10)

class Inventory(models.Model):
    food_item_id=models.AutoField(primary_key=True)
    image=models.ImageField(blank=True)
    food_item_name=models.CharField(max_length=20)
    category=models.CharField(max_length=20)
    description=models.TextField(max_length=100)
    quantity=models.IntegerField(null=True)
    branch=models.CharField(max_length=20)
    sell_price=models.IntegerField(null=False)
    cost_price=models.IntegerField(null=False)
    mfg_date=models.DateField()
    exp_date=models.DateField()


class Table(models.Model):
    STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
    ]

    table_id = models.AutoField(primary_key=True)
    seats = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='vacant')

    def create_tablecart_table(self):
        """Dynamically create a new table for this specific table_id."""
        print(f"DEBUG: Table ID before creating table: {self.table_id}")  # Debug print

        if not self.table_id:  # Ensure table_id is set
            print("ERROR: Table ID is not available. Skipping table creation.")
            return

        table_name = f"table_{self.table_id}_cart"  # Unique table name
        with connection.cursor() as cursor:
            query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                cart_id SERIAL PRIMARY KEY,
                table_id INTEGER REFERENCES adminside_table(table_id) ON DELETE CASCADE,
                order_item TEXT NOT NULL,
                size INTEGER DEFAULT 0,
                quantity INTEGER DEFAULT 0,
                price DECIMAL(10,2) DEFAULT 0.00
            )
            """
            print(f"Executing SQL Query: {query}")  # Debug print
            cursor.execute(query)




    def save(self, *args, **kwargs):
        """Override save to create a unique table dynamically."""
        super().save(*args, **kwargs)
        print(f"DEBUG: Table saved with ID {self.table_id}") 
        self.create_tablecart_table() 

    def __str__(self):
        return f"Table {self.table_id} - {self.status}"


class Sales_reports(models.Model):
  product_id = models.IntegerField(primary_key=True)
  product_name = models.CharField(max_length=50)
  categories= models.CharField(max_length=50)
  quantities= models.IntegerField()
  
class Supplier(models.Model):
  supplier_id = models.IntegerField(primary_key=True)
  supplier_name = models.CharField(max_length=50)
  company_name = models.CharField(max_length=50)
  supplier_email=models.EmailField(max_length=254)
  supplier_phone=PhoneNumberField()
  address= models.CharField(max_length=250)
  branch=models.CharField(max_length=50) 

class Categories(models.Model):
  categories_id = models.IntegerField(primary_key=True)
  categories_name = models.CharField(max_length=50)
  status= models.CharField(max_length=20)

class Customer(models.Model):
  customer_id = models.IntegerField(primary_key=True) 
  customer_firstname = models.CharField(max_length=50)
  customer_lastname = models.CharField(max_length=50)
  customer_email=models.EmailField(max_length=20,blank=True)
  customer_phone=PhoneNumberField()
  gender=models.CharField(max_length=50)

class Staff(models.Model):
  staff_id = models.IntegerField(primary_key=True) 
  staff_username = models.CharField(max_length=50)
  staff_firstname = models.CharField(max_length=50)
  staff_lastname = models.CharField(max_length=50)
  staff_email=models.EmailField(max_length=50)
  staff_phone=PhoneNumberField()
  staff_img=models.ImageField(blank=True)
  staff_role=models.CharField(max_length=50)
  branch=models.CharField(max_length=50)

