# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-29 07:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0005_auto_20180529_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='month_year',
            field=models.CharField(default='', max_length=14, null=True),
        ),
    ]