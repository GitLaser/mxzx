# -*- coding:utf-8 -*-
__author__ = 'chenziang'
__date__ = '2017/5/19 13:51'

from django.conf.urls import url

from .views import OrgView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView,TeacherListView,TeacherDetailView

urlpatterns = [
    # 机构列表
    url(r'^list/$',OrgView.as_view(),name='org_list'),

    # 机构主页
    url(r'^home/(?P<org_id>\d+)$', OrgHomeView.as_view(), name='org_home'),

    # 机构课程
    url(r'^course/(?P<org_id>\d+)$', OrgCourseView.as_view(), name='org_course'),

    # 机构描述
    url(r'^descs/(?P<org_id>\d+)$', OrgDescView.as_view(), name='org_desc'),

    # 机构教师
    url(r'^teacher/(?P<org_id>\d+)$', OrgTeacherView.as_view(), name='org_teacher'),

    # 授课教师
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),

    # 教师详情
    url(r'^teacher_detail/(?P<teacher_id>\d+)$', TeacherDetailView.as_view(), name='teacher_detail'),

    # 机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
]