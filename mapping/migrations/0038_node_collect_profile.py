# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-12 20:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0005_auto_20170212_2001'),
        ('mapping', '0037_auto_20170212_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='collect_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='collect.CollectProfile'),
        ),
    ]
