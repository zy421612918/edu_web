# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-25 16:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180525_1542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailverifyrecord',
            old_name='sendt_ype',
            new_name='send_ype',
        ),
    ]
