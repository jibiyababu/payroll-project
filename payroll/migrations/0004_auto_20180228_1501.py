# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-28 09:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0003_auto_20180228_1456'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='empId',
            new_name='id',
        ),
    ]
