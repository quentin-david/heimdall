# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-10 07:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0019_category_community'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='title',
            field=models.CharField(default='fancy', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='community',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
