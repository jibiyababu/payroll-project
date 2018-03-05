# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-28 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0006_auto_20180228_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='tax_status',
            field=models.CharField(choices=[('NRI', 'NRI'), ('RESIDENT', 'Resident'), ('EXPAT', 'Expat')], default='None', max_length=8),
        ),
    ]
