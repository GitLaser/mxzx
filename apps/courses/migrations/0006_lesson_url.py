# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-07 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='url',
            field=models.URLField(default='', max_length=100, verbose_name='\u8bfe\u7a0b\u94fe\u63a5'),
        ),
    ]
