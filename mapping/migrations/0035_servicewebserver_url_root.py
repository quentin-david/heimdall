# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-29 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapping', '0034_host_foreman_server'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicewebserver',
            name='url_root',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
