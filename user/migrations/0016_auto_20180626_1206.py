# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-26 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_remove_employee_emailid'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='emailid',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
