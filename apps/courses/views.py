# -*- coding:utf-8 -*-
from random import randint
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, PageNotAnInteger

from .models import Course,Video,CourseSource
from operation.models import CourseComment,UserCourse,UserFavorite
from utils.mixin_utils import LoginRequiredMixIn


class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all()
        hot3 = all_courses.order_by('-students')[:3]

        # 搜索功能
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

        # 按学生人数/点击量排名
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses= all_courses.order_by('-click_nums')

        # 对课程列表做分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses,6, request=request)

        courses = p.page(page)

        return render(request,'course-list.html',{'all_courses':courses,'hot3':hot3})


class CourseDetailView(View):
    def get(self, request,course_id):
        course = Course.objects.get(pk=int(course_id))
        chapters_num = course.lesson_set.all().count()
        learners = course.usercourse_set.all()[:5]
        course.click_nums += 1
        course.save()
        tag = course.tag
        if tag:
            other_same_tag_course = Course.objects.filter(tag=tag).exclude(pk=int(course_id))

            if other_same_tag_course:
                recommend_course = other_same_tag_course.order_by('-click_nums')[0]
            else:
                max_num = Course.objects.count()
                recommend_course = Course.objects.get(pk=randint(1, max_num))
        else:
            max_num = Course.objects.count()
            recommend_course = Course.objects.get(pk=randint(1, max_num))

        has_course_faved = False
        # 注意: teacher_id 是字符串，teacher.id 是数字
        if UserFavorite.objects.filter(user=request.user, fav_type=1, fav_id=course.id):
            has_course_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course.course_org.id):
            has_org_faved = True

        return render(request, 'course-detail.html', {'course': course,
                                                      'chapters_num': chapters_num,
                                                      'learners': learners,
                                                      'recommend_course': recommend_course,
                                                      'has_course_faved':has_course_faved,
                                                      'has_org_faved':has_org_faved
                                                      })


class CourseCommentView(LoginRequiredMixIn,View):
    def get(self,request,course_id):
        # 传入course_id，确定是哪门课
        this_course = Course.objects.get(pk=int(course_id))

        # 课程所有的评论
        all_comment = CourseComment.objects.filter(course_id=this_course.id)

        # 课程的老师
        course_teacher = this_course.course_teacher

        # 课程推荐↓
        # 所有含有‘course’的UserCourse的类对象
        user_courses = UserCourse.objects.filter(course=this_course.id)
        # 所有学过‘course’这门课的用户的id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 如果有人学过这门课

        # 学过这门课的同学，还学过以下其他的课，选取第一个，作为推荐课程
        recommend_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course_id=this_course.id)
        if recommend_courses:
            recommend_course = recommend_courses[0]
        else:
            # 如果没人学过这门课,就随机推荐一门课
            max_num = UserCourse.objects.count()-1
            recommend_course = UserCourse.objects.all()[randint(0,max_num)]

        return render(request,'course-comment.html',{'this_course': this_course,
                                                     'all_comment':all_comment,
                                                     'recommend_course':recommend_course,
                                                     'course_teacher':course_teacher})


class CourseVideoView(LoginRequiredMixIn,View):
    def get(self, request, course_id):
        # 传入course_id，确定是哪门课
        this_course = Course.objects.get(pk=int(course_id))
        # 判断用户是否参加了这门课
        has_joined = UserCourse.objects.filter(user=request.user,course=this_course)
        # 没参加，就让他参加
        if not has_joined:
            join_this_course = UserCourse(user=request.user,course=this_course)
            join_this_course.save()
            # 课程学习人数+1
            this_course.students += 1
            this_course.save()

        # 课程所有的评论
        all_comment = CourseComment.objects.all()

        # 课程的老师
        course_teacher = this_course.course_teacher

        # 课程资源
        all_resources = CourseSource.objects.filter(course_id=this_course.id)

        # 学过这门课的同学还学过的其他课
        # 所有含有‘course’的UserCourse的类对象
        user_courses = UserCourse.objects.filter(course=this_course.id)

        # 所有学过‘course’这门课的用户的id
        user_ids = [user_course.user.id for user_course in user_courses]

        # 学过这门课的同学，还学过以下其他的课，选取第一个，作为推荐课程
        recommend_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course_id=this_course.id)
        if recommend_courses:
            recommend_course = recommend_courses[0]
        else:
            # 如果没人学过这门课,就随机推荐一门课
            max_num = UserCourse.objects.count()-1
            recommend_course = UserCourse.objects.all()[randint(0,max_num)]

        return render(request, 'course-video.html', {'this_course': this_course,
                                                        'all_comment': all_comment,
                                                        'recommend_course': recommend_course,
                                                        'course_teacher': course_teacher,
                                                        'all_resources':all_resources,})


class AddCommentView(View):
    # 用户评论
    def post(self,request):
        # 判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录！"}',content_type='application/json')

        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if course_id > 0 and comments:
            course_comments = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comment = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"添加成功！"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败！"}',content_type='application/json')

class VideoPlayView(View):
    # 视频播放页面
    def get(self, request, video_id):
        # 传入video_id，确定是哪个视频
        this_video = Video.objects.get(pk=int(video_id))
        this_course = this_video.lesson.course

        # 课程所有的评论
        all_comment = CourseComment.objects.all()

        # 课程的老师
        course_teacher = this_course.course_teacher

        # 学过这门课的同学还学过的其他课
        # 所有含有‘course’的UserCourse的类对象
        user_courses = UserCourse.objects.filter(course=this_course.id)

        # 所有学过‘course’这门课的用户的id
        user_ids = [user_course.user.id for user_course in user_courses]

        # 学过这门课的同学，还学过以下其他的课，选取第一个，作为推荐课程
        recommend_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(course_id=this_course.id)
        if recommend_courses:
            recommend_course = recommend_courses[0]
        else:
            # 如果没人学过这门课,就随机推荐一门课
            max_num = UserCourse.objects.count()-1
            recommend_course = UserCourse.objects.all()[randint(0,max_num)]

        return render(request, 'video_play.html', {'this_course': this_course,
                                                   'this_video':this_video,
                                                        'all_comment': all_comment,
                                                        'recommend_course': recommend_course,
                                                        'course_teacher': course_teacher})
