# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-05 01:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_is_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='modified_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
