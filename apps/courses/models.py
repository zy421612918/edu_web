# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from orginazition.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    detail = UEditorField(verbose_name=u"课程详情", width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)
    degree = models.CharField(choices=(
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级'),

    ), max_length=2, verbose_name='难度')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name='课程封面', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name='课程点击量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    category = models.CharField(max_length=30, verbose_name='课程类别', default='后端开发')
    course_req = models.CharField(max_length=300, verbose_name='课程须知', default='')
    teacher_tips = models.CharField(max_length=300, verbose_name='老师提示', default='')
    tag = models.CharField(default='', verbose_name='课程标签', max_length=10)
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')



    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):

        return self.lesson_set.all().count()
    get_zj_nums.short_descripton = '章节数'

    def get_course_lesson(self):
        # 获取课程章节信息
        return self.lesson_set.all()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    # 获取章节视频信息
    def get_lesson_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名称')
    url = models.CharField(max_length=200, verbose_name='视频访问地址', default='' )
    add_time = models.DateTimeField(default=datetime.now,  verbose_name=u"添加时间")
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟)')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):

    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    download = models.FileField(upload_to='courses/%Y/%m', verbose_name='资源文件', max_length=100)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
