# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-11 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20170601_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='points',
            field=models.CharField(max_length=150, verbose_name='\u6559\u5b66\u7279\u70b9'),
        ),
    ]
