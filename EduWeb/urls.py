# -*- coding: utf-8 -*-

"""EduWeb URL Configuration

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
from  users import views as user_views
from django.views.static import serve
from EduWeb.settings import MEDIA_ROOT
import xadmin



urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', user_views.IndexView.as_view(), name= 'index'),
    url('^login/$', user_views.LoginView.as_view(), name= 'login'),

    url('^logout/$', user_views.LogOutView.as_view(), name= 'logout'),
    url('^register/$', user_views.registerView.as_view(), name= 'register'),

    # 图片验证码
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', user_views.ActiveUserView.as_view(), name='useractive'),
    url(r'^forget/', user_views.ForgetPwdView.as_view(), name='forgetpwd'),
    url(r'^reset/(?P<active_code>.*)/$', user_views.ResetUserView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', user_views.ModifyPwdView.as_view(), name='modify_pwd'),
    # 课程机构首页


    url(r'^org/', include('orginazition.urls', namespace='org')),
    # 配置文件上传的访问处理
    url(r'^media/(?P<path>.*)$',  serve, {"document_root":MEDIA_ROOT}),


    # 公开课页面
    url(r'^course/', include('courses.urls', namespace='course')),

    # 个人中心转发
    url(r'^users/', include('users.urls', namespace='users')),

    #富文本相关配置

    url(r'^ueditor/', include('DjangoUeditor.urls')),

    # 配置404静态页面访问处理
#   url(r'^static/(?P<path>.*)$',  serve, {"document_root":STATIC_ROOT}),


]



handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'