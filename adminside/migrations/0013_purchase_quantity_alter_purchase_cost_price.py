# Generated by Django 5.1.6 on 2025-03-13 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0012_alter_staff_staff_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='cost_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
