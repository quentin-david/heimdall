# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-28 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0015_auto_20170219_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
