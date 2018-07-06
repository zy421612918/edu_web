#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-5-25


import xadmin
from models import Course,Lesson,Video, CourseResource

class CourseAdmin(object):

    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums','click_nums','add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums','click_nums']
    list_filter =['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums','click_nums','add_time']
    #ordering = ['-click_nums']   #排序规则
    #readonly_fields = ['click_nums']  表示该字段是只读模式
    #exclude = ['click_nums']  表示后台页面不显示字段 但是字段名不能与reaadonly重合
    list_editable = ['degree','desc']  #加入字段可在列表页直接修改对应的信息
    style_fields = {"detail": "ueditor"}



class LessonAdmin(object):

    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):

    list_display = ['lesson', 'name', 'add_time']
    search_fields =  ['lesson', 'name', 'detail']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):

    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']



xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)





