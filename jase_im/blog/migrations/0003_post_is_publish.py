# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-27 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20181127_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_publish',
            field=models.BooleanField(default=False),
        ),
    ]