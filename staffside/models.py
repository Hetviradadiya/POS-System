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
    ordered_items = models.TextField(null=True, blank=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

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
        return f"Sale {self.sales_id} - Table {self.table.table_id} - {self.total_amount} ({self.payment_method}) - Order {self.order_list.order_id}"

    