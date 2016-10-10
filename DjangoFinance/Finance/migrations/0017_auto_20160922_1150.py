# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 03:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0016_fixedincome_annualizedyield'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='说明'),
        ),
        migrations.AddField(
            model_name='agency',
            name='comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='说明'),
        ),
        migrations.AddField(
            model_name='fixedincome',
            name='comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='说明'),
        ),
    ]