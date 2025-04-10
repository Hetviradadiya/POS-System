from django.db import models
from django.utils.timezone import now 
from adminside.models import Table

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)  
    customer = models.ForeignKey("adminside.Customer", on_delete=models.CASCADE, null=True, blank=True)
    ordered_items = models.TextField(null=True, blank=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    branch = models.ForeignKey("adminside.Branch", on_delete=models.CASCADE, null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, null=True, blank=True)
    order_type = models.CharField(max_length=20,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-set branch from the logged-in staff session (if available)
        request = kwargs.pop("request", None)
        if request and "branch_id" in request.session:
            self.branch = request.session["branch_id"]
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Order {self.order_id} - Table {self.table.table_id} - {self.status}"



class Sales(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
    ]

    sales_id = models.AutoField(primary_key=True)
    table = models.ForeignKey('adminside.Table', on_delete=models.CASCADE)  
    order_list = models.ManyToManyField(Order)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')  
    date = models.DateField(auto_now_add=True)  
    time = models.TimeField(auto_now_add=True) 


    def __str__(self):
        orders = ", ".join([str(order.order_id) for order in self.order_list.all()])
        return f"Sale {self.sales_id} - Table {self.table.table_id} - {self.total_amount} ({self.payment_method}) - Orders [{orders}]"

    