#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-5-29



from django.conf.urls import url,include

from . import views


urlpatterns = [
    # 课程课表页
    url(r'^list/$', views.CourselistVie.as_view(), name='course_list'),

    #课程详情页
    url(r'^detail/(?P<course_id>\d+)$', views.CourseDetailView.as_view(), name='course_detail'),

    #课程视频章节
    url(r'^info/(?P<course_id>\d+)$', views.CourseInfoView.as_view(), name='course_info'),

    #课程评论页
    url(r'^comment/(?P<course_id>\d+)$', views.CommentView.as_view(), name='course_coment'),


    #添加课程评论信息
    url(r'^add_comment/$', views.AddCommentVie.as_view(), name='course_addcoment'),



]