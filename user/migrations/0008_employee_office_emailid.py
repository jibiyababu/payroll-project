# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-28 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20180509_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='office_emailid',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
