# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.backends import  ModelBackend
from models import EmailVerifyRecord
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from forms import LoginForm, RegisterForm, ForgetForm,ModifyPwdForm,UploadImageForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import *
from orginazition.models import CourseOrg, Teacher
from courses.models import Course
from pure_pagination import Paginator, PageNotAnInteger
from .models import Banner


class registerView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            #可用UserProfile.objects.create(**register_form.cleaned_data)
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'msg': '用户已经存在'})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name,'register')
            #写入欢迎注册消息

            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册'

            user_message.save()

            return render(request, 'login.html')

        else:

            return render(request, 'register.html',{'register_form':register_form})


class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self, request):
        obj = LoginForm(request.POST)
        if obj.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if not user:

                return render(request, 'login.html', {'msg': '用户名或者密码错误'})
            else:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    print('账户未激活')
                    return render(request, 'login.html', {'msg': '用户未激活'})
        else:

            return render(request, 'login.html', {'obj': obj})


class CustomBackend(ModelBackend):
    """
    重写登录规则，setting中需要配置 AUTHENTICATION_BACKENDS = ('users.views.CustomBackend',} """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user

        except Exception as e:
            return None


class ActiveUserView(View):
    """
    激活用户账户信息
    """
    def get(self, request,active_code):
        all_code = EmailVerifyRecord.objects.filter(code=active_code)
        if all_code:
            for record in all_code:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_faile.html')

        return render(request,'login.html')


class ForgetPwdView(View):
    """
    找回密码
    """
    def get(self, request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')

        else:
            return render(request, 'forgetpwd.html', {'forget_form':forget_form})


class ResetUserView(View):
    """
    重置密码
    """
    def get(self, request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email':email})

        else:
            return render(request, 'active_faile.html')

        return render(request,'login.html')


class ModifyPwdView(View):
    """
    修改用户密码
    """

    def post(self, request):
        print('验证开始')
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():

            print('验证成功')

            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            print('0---->', pwd1,pwd2)
            email = request.POST.get('email', '')

            if pwd1!=pwd2:

                return render(request, 'password_reset.html', {'email': email, 'msg':"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)


            user.save()
            return render(request, 'login.html')
        else:

            print '验证失败'
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """
    个人用户信息

    """
    def get(self, request):

        return render(request,'usercenter-info.html',{})


class UploadView(LoginRequiredMixin, View):
    """
    用户修改头像功能

    """
    def post(self, request):

        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)

        if image_form.is_valid():
            image_form.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse ('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        print('开始验证')

        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            print(pwd1,pwd2)

            if pwd1!=pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            import json

            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):

        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):

            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, 'update_email')

        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(View):
    """
    修改个人邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code =  request.POST.get('code', '')
        print(email,code)
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')

        if existed_records:
            user = request.user
            user.email = email
            user.save()
            existed_records.delete()
            return HttpResponse('{"status":"success"}', content_type='application/json')

        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)


        return render(request, 'usercenter-mycourse.html',{'user_courses':user_courses})


class MyfavOrgView(LoginRequiredMixin, View):
    """
    收藏机构
    """
    def get(self,request):
        org_list =[]
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html',{'org_list':org_list})


class MyfavTeacherView(LoginRequiredMixin, View):
    """
    收藏讲师
    """
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list":teacher_list
        })


class MyfavCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id

            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            "course_list":course_list
        })


class MymessageView(LoginRequiredMixin,View):
    """
    我的消息
    """
    def get(self,request):

        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for un_read_message in all_unread_messages:
            un_read_message.has_read =True
            un_read_message.save()

        #个人消息分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages,5, request=request)

        messages = p.page(page)


        return render(request, 'usercenter-message.html', {
            'messages':messages

        })


class LogOutView(View):
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse

        return redirect(reverse('index'))



class IndexView(View):
    """
    官网首页
    """
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs,



        })


def page_not_found(request):
    # 全局404处理逻辑
    from django.shortcuts import render_to_response

    response =render_to_response('404.html',{})
    response.status_code =404
    return response

def page_error(request):
    # 全局404处理逻辑
    from django.shortcuts import render_to_response

    response =render_to_response('500.html',{})
    response.status_code =500
    return response