# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from orginazition.forms import UserAskForm
from django.shortcuts import render
from operation.models import UserFavorite
from django.views.generic.base import View
from . import models
from courses.models import Course

class OrgListView(View):
    """
    课程机构列表
    """
    def get(self, request):
        # 课程机构
        all_orgs = models.CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_num')[:3]
        #城市
        all_citys = models.CityDict.objects.all()


        # 机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_orgs.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))


        #除筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)
        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        sort =request.GET.get('sort','')
        if sort:
            if sort =='students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_num')
        # 统计数量
        org_num = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs,5, request=request)
        orgs = p.page(page)
        return render(request,'org-list.html', {
            'orgs':orgs,
            'all_citys':all_citys,
            'org_num':org_num,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort,
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):

        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = 'home'
        course_org = models.CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]


        return render(request, 'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        current_page = 'course'
        course_org = models.CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })


class OrgDescView(View):
    """
    机构介绍
    """
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = models.CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html',{
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })


class OrgTeacherView(View):
    """
    机构讲师列表页
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = models.CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html',{
            'all_teacher':all_teacher,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })


class AddFavView(View):
    """
    用户收藏功能
    """
    def post(self , request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            #判断用户是否登录
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))

        if exist_record:
            exist_record.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')


        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) >0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type=int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')



class TeacherListView(View):
    """
    课程讲师列表页
    """
    def get(self, request):

        all_teachers = models.Teacher.objects.all()
        current_nav = 'teacher'

        # 课程讲师搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords)|
                                               Q(work_company__icontains=search_keywords)|
                                               Q(work_position__icontains=search_keywords))

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_num")

        sorted_teacher = models.Teacher.objects.all().order_by("-click_num")[:3]

        #对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)
        return render(request, "teachers-list.html", {
            "all_teachers":teachers,
            "sorted_teacher":sorted_teacher,
            "sort":sort,
            'current_nav':current_nav,
        })



class TeacherDetailView(View):

    def get(self, request, teacher_id):

        teacher = models.Teacher.objects.get(id=int(teacher_id))
        all_courses = Course.objects.filter(teacher=teacher)
        #讲师排行
        sorted_teacher = models.Teacher.objects.all().order_by("-click_num")[:3]


        return render(request, 'teacher-detail.html' ,{
            'teacher':teacher,
            'all_courses':all_courses,
            'sorted_teacher':sorted_teacher
        })
