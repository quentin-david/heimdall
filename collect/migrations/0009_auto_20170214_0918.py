# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-14 09:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0008_auto_20170213_1455'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collect',
            options={'get_latest_by': 'item'},
        ),
    ]
