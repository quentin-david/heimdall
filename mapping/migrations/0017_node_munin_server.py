# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-20 14:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0003_auto_20170120_1434'),
        ('mapping', '0016_auto_20170117_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='munin_server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitoring.Munin'),
        ),
    ]
