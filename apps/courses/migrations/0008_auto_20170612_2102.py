# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-12 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20170607_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='tag',
            field=models.CharField(choices=[('wx', '\u6587\u5b66'), ('kx', '\u79d1\u5b66'), ('IT', 'IT')], default='kx', max_length=10, verbose_name='\u6807\u7b7e'),
        ),
        migrations.AlterField(
            model_name='coursesource',
            name='download',
            field=models.FileField(upload_to='resource/%Y/%m', verbose_name='\u8d44\u6e90\u6587\u4ef6'),
        ),
        migrations.AlterField(
            model_name='coursesource',
            name='name',
            field=models.CharField(max_length=50, verbose_name='\u6587\u4ef6\u540d'),
        ),
    ]
