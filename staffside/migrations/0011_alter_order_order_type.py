# Generated by Django 5.1.6 on 2025-04-09 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffside', '0010_order_order_type_alter_order_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
