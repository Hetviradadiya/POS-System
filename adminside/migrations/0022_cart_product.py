# Generated by Django 5.1.6 on 2025-03-25 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0021_alter_cart_order_item_alter_cart_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(blank=True, db_column='inventory_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='adminside.inventory'),
        ),
    ]
