# -*- coding:utf-8 -*-
__author__ = 'chenziang'
__date__ = '2017/4/22 14:52'

import xadmin

from .models import EmailVerifyRecord,Banner,UserProfile
from xadmin import views
from xadmin.plugins.auth import UserAdmin


class UserProfileAdmin(UserAdmin):
    pass


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = '商业帝国'
    site_footer = '子昂'
    menu_style = 'accordion'
    globe_models_icon = {UserProfile: 'Banner-icon'}


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']
    model_icon = 'fa fa-envelope-open-o'
    readonly_fields = ['send_time','send_type','code','email']
    refresh_times = (3,5,10)
    list_export = ('csv','xls','xml','json')


class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']
    model_icon = 'fa fa-snowflake-o'

# 卸载掉Django本身注册的User
# xadmin.site.unregister(User)


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)

# 注册自己定义的UserProfile
# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSetting)