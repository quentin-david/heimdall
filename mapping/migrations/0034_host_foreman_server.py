# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-29 09:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deployment', '0001_initial'),
        ('mapping', '0033_auto_20170129_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='foreman_server',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='deployment.Foreman'),
            preserve_default=False,
        ),
    ]
