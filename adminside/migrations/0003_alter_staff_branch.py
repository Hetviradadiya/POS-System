# Generated by Django 5.1.6 on 2025-03-07 08:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0002_alter_staff_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='branch',
            field=models.ForeignKey(blank=True, db_column='branch_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminside.branch'),
        ),
    ]
