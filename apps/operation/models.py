# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from users.models import UserProfile
from courses.models import Course




class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    course_name = models.CharField(max_length=50, verbose_name='课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")


    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


class CourseComments(models.Model):

    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程名称')
    comments = models.CharField(max_length=200, verbose_name='评论信息')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '课程名称'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    fav_id = models.IntegerField(default=0, verbose_name='数据ID')
    fav_type = models.IntegerField(choices=(
        (1, '课程'),
        (2, '机构'),
        (3, '老师'),
    ), default=1, verbose_name='收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")


    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):

    user = models.IntegerField(default=0, verbose_name='接受用户')
    message = models.CharField(max_length=200, verbose_name='消息内容')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    has_read = models.BooleanField(max_length=1)


    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='学习的课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name
