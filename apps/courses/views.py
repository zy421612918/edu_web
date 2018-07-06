# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, CourseComments,UserCourse
from courses import models
from utils import mixin_utils
from django.db.models import Q


class CourselistVie(View):

    def get(self,request):
        all_courses =models.Course.objects.all().order_by('-add_time')

        hot_courses = models.Course.objects.all().order_by('-click_nums')[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

        # 课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 对课程分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,3, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html',
                      {'all_courses':courses,
                       'sort':sort,
                       'hot_courses':hot_courses

                       })


class CourseDetailView(View):
    """
    课程详情页
    """

    def get(self, request, course_id):
        course = models.Course.objects.get(id=int(course_id))

        # 增加课程点击数
        course.click_nums += 1
        course.save()

        # 是否收藏课程
        has_fav_course = False
        # 是否收藏机构
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_coures = models.Course.objects.filter(tag=tag)[:1]
        else:
            relate_coures = []
        return render(request, "course-detail.html", {
            "course": course,
            "relate_coures": relate_coures,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org
        })


class CourseInfoView(mixin_utils.LoginRequiredMixin, View):
    """
    课程章节信息

    """

    def get(self, request, course_id):
        course = models.Course.objects.get(id=int(course_id))
        course.students +=1
        course.save()
        # 查询用户是否关联此课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_cousers = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_cousers]
        all_user_courses =UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses =models.Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = models.CourseResource.objects.filter(course=course)


        return render(request, "course-video.html", {
            "course": course,
            'course_resources':all_resources,
            'relate_courses':relate_courses
        })

class CommentView(mixin_utils.LoginRequiredMixin, View):
    """
    课程评论信息
    """
    def get(self, request, course_id):
        course = models.Course.objects.get(id=int(course_id))
        all_resources = models.CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()

        return render(request, "course-comment.html", {
            "course": course,
            'all_comments': all_comments,
            'all_resources':all_resources
        })



class AddCommentVie(View):
    """
    用户添加评论功能
    """
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')


        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments','')
        if course_id >0 and comments:
            course = models.Course.objects.get(id=int(course_id))
            course_comment = CourseComments()
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()


            return HttpResponse('{"status":"success","msg":"添加成功"}',content_type='application/json')

        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}',content_type='application/json')










