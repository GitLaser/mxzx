# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-02 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(choices=[('bx', '\u5927\u5b66\u5fc5\u4fee'), ('xx', '\u5927\u5b66\u9009\u4fee')], default='bx', max_length=30, verbose_name='\u8bfe\u7a0b\u7c7b\u522b'),
        ),
    ]