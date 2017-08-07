#-*- coding:utf-8 -*-
__author__ = 'chenziang'
__date__ = '2017/4/23 15:10'
import xadmin

from .models import CourseComment,UserCourse,UserFavorite,UserMessage



class CourseCommentAdmin(object):
    list_display = ['user','course','comment','add_time']
    search_fields = ['user','course','comment']
    list_filter = ['user','course','comment','add_time']
    model_icon = 'fa fa-comments'


class UserFavoriteAdmin(object):
    list_display = ['user','fav_id','fav_type','add_time']
    search_fields = ['user','fav_id','fav_type']
    list_filter = ['user','fav_id','fav_type','add_time']


class UserMessageAdmin(object):
    list_display = ['user','message','has_read','add_time']
    search_fields = ['user','message','has_read']
    list_filter = ['user','message','has_read','add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']



xadmin.site.register(CourseComment,CourseCommentAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)