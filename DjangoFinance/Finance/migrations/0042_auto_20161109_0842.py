# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-09 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0041_equityposition_cost'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equity',
            options={'ordering': ['Type', 'Code'], 'verbose_name': '权益类行情', 'verbose_name_plural': '权益类行情'},
        ),
        migrations.AddField(
            model_name='equityposition',
            name='AllGain',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='累计收益'),
        ),
        migrations.AddField(
            model_name='equityposition',
            name='CurrentPrice',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='现价'),
        ),
        migrations.AddField(
            model_name='equityposition',
            name='MarketValue',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='市值'),
        ),
        migrations.AddField(
            model_name='equityposition',
            name='ReturnRate',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='当前收益率'),
        ),
    ]