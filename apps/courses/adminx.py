# -*- coding:utf-8 -*-
__author__ = 'chenziang'
__date__ = '2017/4/23 14:19'

import xadmin
from .models import Course,CourseSource,Video,Lesson,BannerCourse


class LessonInLine(object):
    model = Lesson
    extra = 0


class CourseSourceInLine(object):
    model = CourseSource
    extra = 0


class CourseAdmin(object):
    list_display = ['name','course_org','desc','detail','degree','is_banner','learn_time','students','fav_nums','click_nums']
    search_fields = ['name','course_org','desc','detail','degree','learn_time','students','fav_nums','click_nums']
    list_filter = ['name','course_org','desc','detail','degree','learn_time','students','fav_nums','click_nums']
    readonly_fields = ['students','click_nums','add_time']
    exclude = ['fav_nums']
    model_icon = 'fa fa-book'
    inlines = [LessonInLine,CourseSourceInLine]

    def queryset(self):
        qs = super(CourseAdmin,self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.courses_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class LessonAdmin(object):
    list_display = ['course','name',]
    search_fields = ['course','name']
    list_filter = ['course','name']
    model_icon = 'fa fa-bars'


class VideoAdmin(object):
    list_display = ['lesson','name']
    search_fields = ['course','name']
    list_filter = ['lesson','name']
    model_icon = 'fa fa-film'


class CourseSourceAdmin(object):
    list_display = ['course','name','download']
    search_fields = ['course','name']
    list_filter = ['course','name','download']
    model_icon = 'fa fa-file'


class BannerCourseAdmin(object):
    list_display = ['name','course_org','desc','detail','degree','is_banner','learn_time','students','fav_nums','click_nums']
    search_fields = ['name','course_org','desc','detail','degree','learn_time','students','fav_nums','click_nums']
    list_filter = ['name','course_org','desc','detail','degree','learn_time','students','fav_nums','click_nums']
    readonly_fields = ['students','fav_nums','click_nums','add_time']
    inlines = [LessonInLine,CourseSourceInLine]

    def queryset(self):
        qs = super(BannerCourseAdmin,self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseSource,CourseSourceAdmin)