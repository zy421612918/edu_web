# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from datetime import datetime


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市')
    desc = models.CharField(max_length=200, default='', verbose_name='城市描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name='机构名称')
    desc = models.TextField(verbose_name='机构描述')
    category = models.CharField(max_length=20,choices=(
        ('pxjg','培训机构'),
        ('gr','个人'),
        ('gx','高校'),
    ), verbose_name='培训机构', default='pxjg')
    click_num = models.IntegerField(default=0, verbose_name='点击量')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数量')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='机构LOGO', max_length=100)
    address = models.CharField(max_length=100, verbose_name='机构地址')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    city = models.ForeignKey(CityDict, verbose_name = '所在城市')
    course_num = models.IntegerField(default=0, verbose_name='课程数量')
    tag = models.CharField(default='全国知名', verbose_name='机构标签', max_length=10)

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name
    # 获取课程讲师数量
    def get_teacher_nums(self):
        return self.teacher_set.all().count()
    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构')
    name = models.CharField(max_length=10, verbose_name='教师名字')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='担任职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_num = models.IntegerField(default=0, verbose_name='点击量')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name='老师头像', max_length=100 ,default='')

    class Meta:
        verbose_name = '教师信息'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

    def get_course_nums(self):

        return self.course_set.all().count()








