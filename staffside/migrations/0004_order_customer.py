# Generated by Django 5.1.6 on 2025-04-02 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffside', '0003_rename_created_on_order_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
