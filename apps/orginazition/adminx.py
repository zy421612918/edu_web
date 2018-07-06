#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-5-25


import xadmin

from models import CityDict,CourseOrg,Teacher

class CityDictAdmin(object):

    list_display = ['name', 'desc', 'add_time']
    search_fields =  ['name', 'desc']
    list_filter =  ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):


    list_display = ['name', 'desc', 'click_num', 'fav_nums', 'image', 'address', 'city']
    search_fields = ['name', 'desc', 'click_num', 'fav_nums', 'image', 'address', 'city']
    list_filter = ['name', 'desc', 'click_num', 'fav_nums', 'image', 'address', 'city__name']
    relfield_style = 'fk-ajax'  #表示能够搜索方式显示字段




class TeacherAdmin(object):


    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num','fav_nums','add_time']
    search_fields =  ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num','fav_nums']
    list_filter =  ['org__name', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num','fav_nums','add_time']


xadmin.site.register( CityDict,CityDictAdmin)
xadmin.site.register( CourseOrg,CourseOrgAdmin)
xadmin.site.register( Teacher,TeacherAdmin)
