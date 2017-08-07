# -*-coding:utf-8-*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

from organization.models import Org,Teacher


class Course(models.Model):
    course_org = models.ForeignKey(Org,verbose_name=u'所属大学',null=True)
    course_teacher = models.ForeignKey(Teacher,verbose_name=u'任课教师',null=True)
    name = models.CharField(max_length=50,verbose_name=u'课程名')
    desc = models.CharField(max_length=300,verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(verbose_name=u'难度' ,choices=(('cj',u'初级'),('zj',u'中级'),('gj',u'高级')), max_length=10)
    category = models.CharField(max_length=30,verbose_name=u'课程类别',choices=(('bx',u'大学必修'),('xx',u'大学选修')),default='bx')
    learn_time = models.IntegerField(default=0,verbose_name=u'学习时长(h)')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏人数')
    tag = models.CharField(default='kx',choices=(('wx',u'文学'),('kx',u'科学'),('IT',u'IT')),max_length=10,verbose_name=u'标签')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name=u'封面图',max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    is_banner = models.BooleanField(default=False,verbose_name=u'是否首页轮播')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __unicode__(self):
        return self.name

    def get_all_lessons(self):
        return self.lesson_set.all()

    # 得到机构课程总数
    def get_lesson_nums(self):
        return self.lesson_set.all().count()

    def get_all_sourses(self):
        return self.coursesource_set.all()


class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100,verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def get_all_videos(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u'章节')
    name = models.CharField(max_length=50,verbose_name=u'视频名')
    url = models.URLField(max_length=100, default='', verbose_name=u'课程链接')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

class CourseSource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=50, verbose_name=u'文件名')
    download = models.FileField(upload_to='resource/%Y/%m',verbose_name=u'资源文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name


class BannerCourse(Course):
    class Meta:
        verbose_name = u'首页轮播课程'
        verbose_name_plural = verbose_name
        proxy = True