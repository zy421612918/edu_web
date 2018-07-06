#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-5-28



from django.conf.urls import url,include
from orginazition import views

urlpatterns = [

#课程机构首页
    url(r'^list/$', views.OrgListView.as_view(), name='org_list'),

    url(r'^add_ask/$',views.AddUserAskView.as_view(), name='add_ask'),

    url(r'^home/(?P<org_id>\d+)/$',views.OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$',views.OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$',views.OrgDescView.as_view(), name='org_decs'),


    url(r'^org_teacher/(?P<org_id>\d+)/$',views.OrgTeacherView.as_view(), name='org_teacher'),


    # 机构收藏功能
    url(r'^add_fav/$',views.AddFavView.as_view(), name='add_fav'),

    #讲师列表页
    url(r'^teacher/list/$', views.TeacherListView.as_view(), name="teacher_list"),

    # 讲师详情页

    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', views.TeacherDetailView.as_view(), name='teacher_detal'),

]

