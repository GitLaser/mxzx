# -*- coding:utf-8 -*-
import json
from django.shortcuts import render,render_to_response
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_mail,send_forgetpwd_mail,send_update_mail
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse


from utils.mixin_utils import LoginRequiredMixIn
from pure_pagination import Paginator, PageNotAnInteger

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm,ResetPwdForm,UploadImageForm,UserInfoForm
from courses.models import Course
from organization.models import Org,Teacher
from operation.models import UserCourse,UserFavorite,UserMessage


# 重写 authenticated 认证
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 为了可以用邮箱名注册，我们这样：
            user = UserProfile.objects.get(Q(username=username)|Q(email=username),)
            if user.check_password(password) :
                return user
        except Exception as e:
            return None


class LoginView(View):
    #登录
    def get(self,request):
        return render(request, 'login.html', {})

    def post(self,request):

        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            # 做认证
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    # 登录
                    login(request, user)
                    # 登陆成功返回首页
                    # reverse('index') 等于'/'
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户尚未激活！', 'login_form': login_form})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误！', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'msg': '用户名或密码错误！', 'login_form': login_form})


# 用户退出
class LogOutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/')


def register_view(request):
    # 用户注册
    if request.POST:
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            password = request.POST.get('password', '')
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html',{'msg':'用户已存在'})
            else:
                user_profile = UserProfile()
                user_profile.username = username
                user_profile.email = username
                user_profile.password = make_password(password)
                user_profile.is_active = False
                user_profile.save()

                # 给用户发一条欢迎加入的消息
                user_message = UserMessage(user=user_profile, message=u'欢迎加入本站！学习交流请+q：690216037')
                user_message.save()

                # 发送注册邮件
                send_register_mail(email=username)
                return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})
    else:
        register_form = RegisterForm()
    return render(request, 'register.html')


class ActivateUserView(View):
    # 激活用户
    def get(self,request,activate_code):
        all_records = EmailVerifyRecord.objects.filter(code=activate_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ForgetPwdView(View):
    # 点击登录页面的忘记密码，执行此处
    def get(self,request):
        return render(request,'forget_pwd.html')

    def post(self,request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        if forget_pwd_form.is_valid():
            email = request.POST.get('email','')
            if UserProfile.objects.filter(email=email):
                send_forgetpwd_mail(email)
                return render(request, 'send_success.html',{})
            else:
                return render(request,'forget_pwd.html', {'msg': '用户不存在！'})
        else:
            return render(request, 'forget_pwd.html', {'msg': '输入有误！'})


class RedirectToResetView(View):
    # 打开邮箱里重置密码的链接，执行此处，跳转到密码重置页面
    def get(self, request,activate_code):
        record = EmailVerifyRecord.objects.get(code=activate_code)
        email = record.email
        # 将邮箱号传到重置页面，以便设置的时候知道是哪个用户
        return render(request,'password_reset.html',{'email':email})


class ResetPwdView(View):
    def post(self, request):
        reset_password_form = ResetPwdForm(request.POST)
        if reset_password_form.is_valid():
            username = request.POST.get('email', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 == password2:
                user = UserProfile.objects.get(username=username)
                user.password = make_password(password2)
                user.save()
                return render(request,'login.html',{'msg':'密码设置成功，请登录！'})
            else:
                return render(request,'password_reset.html',{'msg':'两次输入的密码不相同！'})
        else:
            return render(request,'password_reset.html',{'reset_password_form':reset_password_form})


class IndexView(View):
    def get(self,request):
        show_courses = Course.objects.filter(is_banner=False).order_by('-click_nums')[:6]
        banner_courses = Course.objects.filter(is_banner=True)
        show_orgs = Org.objects.all()
        return render(request,'index.html',{'show_courses':show_courses,'show_orgs':show_orgs,'banner_courses':banner_courses})


def no_authority_403(request):
    response = render_to_response('403.html')
    response.status_code = 403
    return  response


def page_not_found_404(request):
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def server_error_500(request):
    response = render_to_response('500.html')
    response.status_code = 500
    return response


class UploadImageView(LoginRequiredMixIn, View):
    # 修改头像
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()


# 用户个人信息
class UserInfoView(LoginRequiredMixIn, View):
    def get(self, request):
        return render(request, 'usercenter-info.html')

    # 用户修改昵称，手机号，地址，生日
    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        res = dict()

        if user_info_form.is_valid():
            user_info_form.save()
            res['status'] = 'success'

        else:
            res = user_info_form.errors

        return HttpResponse(json.dumps(res), content_type='application/json')


# 用户在个人中心修改密码
class UpdatePwdView(LoginRequiredMixIn, View):
    def post(self, request):
        modify_form = ResetPwdForm(request.POST)
        res = dict()

        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                res['status'] = 'fail'
                res['msg'] = '两次密码不一致'
                return HttpResponse(json.dumps(res), content_type='application/json')

            user = request.user
            user.password = make_password(pwd2)
            user.save()

            res['status'] = 'success'
            res['msg'] = '密码修改成功'
        else:
            res = modify_form.errors

        return HttpResponse(json.dumps(res), content_type='application/json')


# 个人中心，发送邮箱验证码
class SendEmailCodeView(LoginRequiredMixIn,View):
    def get(self,request):
        email = request.GET.get('email','')
        res = dict()
        if UserProfile.objects.filter(email=email):
            res['email'] = '邮箱已注册'
            return HttpResponse(json.dumps(res), content_type='application/json')
        send_update_mail(email=email)
        res['status'] = 'success'
        res['msg'] = '发送验证码成功'
        return HttpResponse(json.dumps(res), content_type='application/json')


# 修改个人邮箱
class UpdateEmailView(LoginRequiredMixIn, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update')
        res = dict()
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            res['status'] = 'success'
            res['msg'] = '邮箱修改成功！'
        else:
            res['status'] = 'fail'
            res['msg'] = '验证码出错！'

        return HttpResponse(json.dumps(res), content_type='application/json')


class MyCourseView(LoginRequiredMixIn, View):
    def get(self,request):
        user = request.user
        usercourse_objects = UserCourse.objects.filter(user=int(user.id))
        user_courses = []
        for obj in usercourse_objects.all():
            user_courses.append(obj.course)
        return render(request,'usercenter-mycourse.html',{'user_courses':user_courses})


class MyFavOrgView(View):
    def get(self,request):
        userfavorite_objs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        fav_orgs = []
        for obj in userfavorite_objs:
            org = Org.objects.get(id=obj.fav_id)
            fav_orgs.append(org)
        return render(request,'usercenter-fav-org.html',{'fav_orgs':fav_orgs})


class MyFavTeacherView(View):
    def get(self,request):
        userfavorite_objs = UserFavorite.objects.filter(user=request.user,fav_type=3)
        fav_teachers = []
        for obj in userfavorite_objs:
            teacher = Teacher.objects.get(id=obj.fav_id)
            fav_teachers.append(teacher)
        return render(request,'usercenter-fav-teacher.html',{'fav_teachers':fav_teachers})


class MyFavCourseView(View):
    def get(self,request):
        userfavorite_objs = UserFavorite.objects.filter(user=request.user,fav_type=1)
        fav_courses = []
        for obj in userfavorite_objs:
            course = Course.objects.get(id=obj.fav_id)
            fav_courses.append(course)
        return render(request,'usercenter-fav-course.html',{'fav_courses':fav_courses})


class MyMessageView(View):
    def get(self,request):
        all_messages = UserMessage.objects.filter(user=request.user)

        # 用户来到消息页面，就自动把所有未读消息变为已读
        for message in all_messages:
            message.has_read = True
            message.save()
        # 我的消息，分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages,6, request=request)

        messages = p.page(page)


        return render(request,'usercenter-message.html',{'messages':messages})