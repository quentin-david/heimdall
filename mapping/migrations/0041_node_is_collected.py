# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-15 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapping', '0040_node_collect_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='is_collected',
            field=models.BooleanField(default=True),
        ),
    ]
