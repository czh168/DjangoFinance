# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 03:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0015_auto_20160922_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixedincome',
            name='annualizedyield',
            field=models.FloatField(blank=True, null=True, verbose_name='年化率'),
        ),
    ]
