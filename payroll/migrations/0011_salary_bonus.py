# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-06-08 05:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0010_auto_20180606_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='bonus',
            field=models.IntegerField(default=0),
        ),
    ]
