# -*-coding:utf-8-*-
from __future__ import unicode_literals
from datetime import datetime


from django.db import models

from users.models import UserProfile
from courses.models import Course


class CourseComment(models.Model):
    # 用户对课程的评论
    user = models.ForeignKey(UserProfile,verbose_name=u'用户')
    course = models.ForeignKey(Course,verbose_name=u'课程')
    comment = models.CharField(max_length=200,verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'课程评论'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name=u'用户')
    # ID 是课程的 ID 或者是 讲师、课程机构的 ID
    fav_id = models.IntegerField(default=0,verbose_name=u'数据id')
    fav_type = models.IntegerField(choices=((1, '课程'),(2, '大学'),(3, '讲师')), verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    # 如果 为 0 代表全局消息，否则就是用户的 ID
    user = models.ForeignKey(UserProfile,verbose_name=u'接收用户')
    message = models.CharField(max_length=500,verbose_name=u'消息')
    has_read = models.BooleanField(default=False,verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    # 用户参加过哪些课程
    user = models.ForeignKey(UserProfile,verbose_name=u'用户')
    course = models.ForeignKey(Course,verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'用户课程'
        verbose_name_plural = verbose_name

