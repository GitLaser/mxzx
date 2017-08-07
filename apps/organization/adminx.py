#-*- coding:utf-8 -*-
__author__ = 'chenziang'
__date__ = '2017/4/23 14:55'
import xadmin

from .models import CityDict, Org, Teacher


# 城市
class CityDictAdmin(object):
    list_display = ['name','desc',]
    search_fields = ['name','desc']
    list_filter = ['name','desc',]
    model_icon = 'fa fa-building'
    fields_style = 'fk-ajax'


# 机构
class OrgAdmin(object):
    list_display = ['name','desc','city','click_nums','fav_nums','address',]
    search_fields = ['name','desc','city','click_nums','fav_nums','address']
    list_filter = ['name','desc','city','click_nums','fav_nums','address',]


# 讲师
class TeacherAdmin(object):
    list_display = ['name','org','teach','work_year','work_position','points','click_nums','fav_nums']
    search_fields = ['name','org','teach','work_year','work_position','points','click_nums','fav_nums']
    list_filter = ['name','org','work_year','work_position','points','click_nums','fav_nums']


xadmin.site.register(Org, OrgAdmin)
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(Teacher, TeacherAdmin)