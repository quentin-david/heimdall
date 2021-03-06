# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-09 14:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import notes.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0016_auto_20170228_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_add', models.BooleanField(default=True)),
                ('can_edit', models.BooleanField(default=False)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.Community')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='notesfile',
            name='uploaded_file',
            field=models.FileField(blank=True, null=True, upload_to=notes.models.file_naming),
        ),
        migrations.AddField(
            model_name='community',
            name='community_users',
            field=models.ManyToManyField(related_name='contributors', through='notes.CommunityUsers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='community',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
