# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-10 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0021_auto_20170410_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='communityusers',
            name='user_visa',
            field=models.BooleanField(default=True),
        ),
    ]
