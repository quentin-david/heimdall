# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-19 12:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0014_auto_20170219_1027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notes',
            name='uploaded_files',
        ),
        migrations.AddField(
            model_name='notesfile',
            name='notes',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='notes.Notes'),
            preserve_default=False,
        ),
    ]
