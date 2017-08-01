# -*- coding:utf-8 -*-
__author__ = 'chenziang'
__date__ = '2017/6/10 19:54'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixIn(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixIn,self).dispatch(request,*args,**kwargs)