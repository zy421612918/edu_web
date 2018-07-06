#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-5-25

import xadmin
from xadmin import views
from models import UserProfile, EmailVerifyRecord,Banner

class BaseSetting(object):
    """
    主题
    """
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    """
    后台页面标题的修改配置，底部的信息配置
    """
    site_title = '某教育官网后台管理'
    site_footer = '在线教育网'
    menu_style = 'accordion'

class UserProfileAdmin(object):

    list_display = ['nickname', 'birday', 'gender', 'address', 'mobile', 'image']
    search_fields = ['nickname', 'birday', 'gender', 'address', 'mobile', 'image']
    list_filter = ['nickname', 'birday', 'gender', 'address', 'mobile', 'image']


class EmailVerifyRecordAdmin(object):

    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-address-book-o'   #自定义图标

class BannerAdmin(object):

    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
    model_icon = 'fa fa-cloud'


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)   #配置xadmin全局的样式，固定写法

xadmin.site.register(views.CommAdminView, GlobalSettings)  # 配置页头页脚的文字显示信息，固定写法









