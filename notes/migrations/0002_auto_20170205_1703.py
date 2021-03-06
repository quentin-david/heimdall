# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='public',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='notes',
            name='shared',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notes',
            name='state',
            field=models.CharField(choices=[('draft', 'Draft'), ('info', 'Info')], max_length=15),
        ),
    ]
