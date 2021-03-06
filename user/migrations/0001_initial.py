# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-30 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('passWord', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=40)),
                ('create_time', models.DateTimeField(verbose_name='date published')),
                ('update_time', models.DateTimeField(verbose_name='date published')),
                ('integral', models.IntegerField(default=0)),
            ],
        ),
    ]
