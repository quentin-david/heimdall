# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-12 19:47
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapping', '0037_auto_20170212_1109'),
        ('collect', '0003_auto_20170212_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField()),
                ('data_file', models.TextField()),
                ('data_json', django.contrib.postgres.fields.jsonb.JSONField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collect.CollectItem')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapping.Node')),
            ],
        ),
    ]
