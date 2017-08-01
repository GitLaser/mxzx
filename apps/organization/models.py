#-*-coding:utf-8-*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models


class CityDict(models.Model):
    name = models.CharField(max_length=20,verbose_name=u'城市名')
    desc = models.CharField(max_length=209,verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Org(models.Model):
    name = models.CharField(max_length=50,verbose_name=u'大学名称')
    city = models.ForeignKey(CityDict,verbose_name=u'所在城市')
    desc = models.TextField(verbose_name=u'描述')
    click_nums = models.IntegerField(default=0,verbose_name=u'点击量')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏数')
    image = models.ImageField(upload_to='org/%Y/%m',verbose_name=u'logo',max_length=100)
    address = models.CharField(max_length=150,verbose_name=u'地址')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    courses_nums = models.IntegerField(default=0,verbose_name=u'课程数')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Teacher(models.Model):
    org = models.ForeignKey(Org,verbose_name=u'所属大学')
    name = models.CharField(max_length=50, verbose_name=u'教师名字')
    photo = models.ImageField(max_length=100,verbose_name=u'教师照片',upload_to='teacher/%Y',null=True)
    teach = models.CharField(max_length=50,verbose_name=u'任课',null=True)
    work_year = models.IntegerField(default=0,verbose_name=u'工作年限')
    work_position = models.CharField(max_length=100,verbose_name=u'职位')
    points = models.CharField(max_length=150,verbose_name=u'教学特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击量')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'讲师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name