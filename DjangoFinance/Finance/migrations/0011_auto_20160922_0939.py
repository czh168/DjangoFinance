# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 01:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0010_auto_20160922_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixedincome',
            name='buydate',
            field=models.DateField(null=True, verbose_name='购入时间'),
        ),
    ]