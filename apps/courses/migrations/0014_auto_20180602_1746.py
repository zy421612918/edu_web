# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-02 17:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20180602_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='tag',
            field=models.CharField(default='\u5168\u56fd\u77e5\u540d', max_length=10, verbose_name='\u8bfe\u7a0b\u6807\u7b7e'),
        ),
    ]
