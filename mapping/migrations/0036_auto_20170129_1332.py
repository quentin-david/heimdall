# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-29 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapping', '0035_servicewebserver_url_root'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicewebserver',
            name='url_root',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
