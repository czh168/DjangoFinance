# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 01:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0014_auto_20160922_0952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='investtype',
            options={'ordering': ['name', 'subname'], 'verbose_name': '投资类别', 'verbose_name_plural': '投资类别'},
        ),
    ]