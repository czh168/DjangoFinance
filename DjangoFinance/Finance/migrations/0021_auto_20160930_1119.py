# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0020_fixedincomecashflow'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fixedincomecashflow',
            options={'ordering': ['happenddate'], 'verbose_name': '固定收益类现金流', 'verbose_name_plural': '固定收益类现金流'},
        ),
        migrations.AddField(
            model_name='fixedincome',
            name='discount',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='优惠'),
        ),
        migrations.AlterField(
            model_name='fixedincome',
            name='spend',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='投入'),
        ),
    ]
