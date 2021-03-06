# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 00:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0004_auto_20160922_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='investtype',
            name='comment',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='说明'),
        ),
        migrations.AddField(
            model_name='investtype',
            name='liquidity',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='流动性'),
        ),
        migrations.AddField(
            model_name='investtype',
            name='risk',
            field=models.CharField(blank=True, choices=[('1', '低'), ('2', '中'), ('3', '高')], max_length=1, null=True, verbose_name='风险'),
        ),
    ]
