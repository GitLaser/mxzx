# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-22 12:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0006_auto_20170717_1035'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserAsk',
        ),
        migrations.AlterField(
            model_name='usermessage',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u63a5\u6536\u7528\u6237'),
        ),
    ]
