# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-23 15:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190322_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagehostingmodel',
            name='format',
            field=models.CharField(default='jpeg', max_length=32),
        ),
        migrations.AlterField(
            model_name='imagehostingmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
