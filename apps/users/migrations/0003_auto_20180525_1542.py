# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-25 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180525_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='sendt_ype',
            field=models.CharField(choices=[('register', '\u6ce8\u518c'), ('forget', '\u627e\u56de\u5bc6\u7801')], max_length=10, verbose_name='\u9a8c\u8bc1\u7801\u7c7b\u578b'),
        ),
    ]
