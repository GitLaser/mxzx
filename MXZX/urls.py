# -*- coding:utf-8 -*-
"""MXZX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url,include
import xadmin
from users.views import LoginView,register_view,ActivateUserView,ForgetPwdView,RedirectToResetView,\
    ResetPwdView,IndexView,LogOutView

from django.views.static import serve
from MXZX.settings import MEDIA_ROOT


urlpatterns = [

    # 后台管理
    url(r'^xadmin/', xadmin.site.urls),

    # 首页
    url(r'^$',IndexView.as_view(), name='index'),

    # 登录
    url(r'^login/$',LoginView.as_view(), name='login'),

    # 注册页面
    url(r'^register/$',register_view, name='register'),

    # 登出
    url(r'^logout/$',LogOutView.as_view(), name='logout'),

    # 校验码
    url(r'^captcha/', include('captcha.urls')),

    # 激活用户
    url(r'^activate/(?P<activate_code>.*)/$', ActivateUserView.as_view(), name='ActivateUser'),

    # 忘记密码
    url(r'^forget_pwd/$',ForgetPwdView.as_view(), name='forget_pwd'),

    # 打开邮箱里重置密码的链接，执行此处，跳转到密码重置页面
    url(r'^RedirectToReset/(?P<activate_code>.*)/$', RedirectToResetView.as_view(), name='RedirectToReset'),

    # 重置密码
    url(r'^resetpwd',ResetPwdView.as_view(), name='resetpwd'),

    # 机构相关的url配置
    url(r'^org/',include('organization.urls', namespace='org')),

    # 课程相关url
    url(r'course/',include('courses.urls', namespace='course')),

    # 用户相关url
    url(r'user/', include('users.urls', namespace='user')),

    # 当debug=true
    url(r'^media/(?P<path>.*)', serve, {'document_root':MEDIA_ROOT}),

    # 当debug=false
    # url(r'^static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}),
]
