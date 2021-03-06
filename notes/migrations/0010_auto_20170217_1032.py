# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-17 10:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0009_bookmark_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='notes.Category'),
        ),
    ]
