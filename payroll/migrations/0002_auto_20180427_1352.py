# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-27 08:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salary',
            old_name='paid_days',
            new_name='working_days',
        ),
    ]
