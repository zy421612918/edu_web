# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-30 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20180530_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default='', max_length=10, verbose_name='\u8bfe\u7a0b\u6807\u7b7e'),
        ),
    ]