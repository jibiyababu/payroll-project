# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-05 06:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0023_auto_20180305_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='salary',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
