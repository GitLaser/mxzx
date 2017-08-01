# -*- coding:utf-8 -*-
__author__ = 'chenziang'
__date__ = '2017/5/30 13:22'

from django.conf.urls import url
from .views import CourseCommentView,CourseDetailView,CourseListView,CourseVideoView,AddCommentView,VideoPlayView

urlpatterns = [
    # 课程列表页
    url(r'^list/$',CourseListView.as_view(),name='course_list'),

    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),

    # 课程评论
    url(r'^comment/(?P<course_id>\d+)/$',CourseCommentView.as_view(),name='course_comment'),

    # 课程视频
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name='course_video'),

    # 添加课程评论
    url(r'^add_comment//$', AddCommentView.as_view(), name='add_comment'),

    # 播放视频地址
    url(r'^video_play/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),
]