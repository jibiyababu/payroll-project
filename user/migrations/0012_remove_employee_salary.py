# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-13 06:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_salary_increment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='salary',
        ),
    ]
