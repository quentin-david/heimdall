# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-15 16:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapping', '0007_auto_20170115_1538'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nodeparams',
            name='node_ptr',
        ),
        migrations.DeleteModel(
            name='NodeParams',
        ),
    ]
