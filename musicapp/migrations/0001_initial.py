# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-24 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uri', models.CharField(max_length=200, unique=True)),
                ('lyrics', models.TextField(default=None, null=True)),
                ('artist', models.CharField(max_length=200, null=True)),
                ('title', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
