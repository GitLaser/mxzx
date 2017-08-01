# -*- coding:utf-8 -*-
__author__ = 'chenziang'
__date__ = '2017/6/17 21:13'

from django.conf.urls import url
from .views import UserInfoView,MyCourseView,UploadImageView,UpdatePwdView,SendEmailCodeView,\
    UpdateEmailView,MyFavOrgView,MyFavCourseView,MyFavTeacherView,MyMessageView

urlpatterns = [
    # 用户个人中心
    url(r'^info_center/$',UserInfoView.as_view(),name='info_center'),

    # 我的课程
    url(r'^my_course/$', MyCourseView.as_view(), name='my_course'),

    # 我收藏的大学
    url(r'^my_fav_org/$', MyFavOrgView.as_view(), name='my_fav_org'),

    # 我收藏的教师
    url(r'^my_fav_teacher/$', MyFavTeacherView.as_view(), name='my_fav_teacher'),

    # 我收藏的课程
    url(r'^my_fav_course/$', MyFavCourseView.as_view(), name='my_fav_course'),

    # 我的消息
    url(r'^my_message/$', MyMessageView.as_view(), name='my_message'),

    # 修改头像
    url(r'^upload_image/$', UploadImageView.as_view(), name='upload_image'),

    # 修改password
    url(r'^update_pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 发送邮箱验证码（个人中心）
    url(r'^send_code/$', SendEmailCodeView.as_view(), name='send_code'),

    # 就修改绑定邮箱（个人中心）
    url(r'^update_email/$',UpdateEmailView.as_view(),name='update_email')
]