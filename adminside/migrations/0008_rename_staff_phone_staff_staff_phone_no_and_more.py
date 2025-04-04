# Generated by Django 5.1.6 on 2025-03-12 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0007_alter_customer_customer_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='staff_phone',
            new_name='staff_phone_no',
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_email',
            field=models.EmailField(max_length=50, unique=True),
        ),
    ]
