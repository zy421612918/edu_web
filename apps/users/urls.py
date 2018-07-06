#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-5-31

import views


from django.conf.urls import url,include

urlpatterns = [
    # 用户信息
    url(r'^info/$',views.UserInfoView.as_view(), name='user_info'),

    #用户头像上传
    url(r'^image/upload/$', views.UploadView.as_view(), name='image_upload'),

    #用户个人中心修改密码
    url(r'^update/pwd/$', views.UpdatePwdView.as_view(), name="update_pwd"),

    #发送邮箱验证码
    url(r'^sendemail_code/$', views.SendEmailCodeView.as_view(), name="sendemail_code"),

    # 修改邮箱
    url(r'^update_email/$', views.UpdateEmailView.as_view(), name="update_email"),

    #我的课程
    url(r'^mycourse/$', views.MyCourseView.as_view(), name="mycourse"),

    # 我的收藏机构
    url(r'^myfav/org/$', views.MyfavOrgView.as_view(), name="myfav_org"),

    # 我的授课讲师
    url(r'^myfav/teacher/$', views.MyfavTeacherView.as_view(), name="myfav_teacher"),

    # 我的课程
    url(r'^myfav/course/$', views.MyfavCourseView.as_view(), name="myfav_course"),

    # 我的消息中心
    url(r'^mymessage/$', views.MymessageView.as_view(), name="mymessage"),






]