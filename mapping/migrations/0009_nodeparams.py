# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-15 16:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapping', '0008_auto_20170115_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='NodeParams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_check', models.DateField(auto_now=True)),
                ('ip_public', models.GenericIPAddressField(null=True)),
                ('ip_admin', models.GenericIPAddressField()),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapping.Node')),
            ],
        ),
    ]
