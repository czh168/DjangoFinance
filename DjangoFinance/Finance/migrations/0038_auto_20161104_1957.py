# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-04 11:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0037_equitypositionstatu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equitypositionstatu',
            name='EquityReg',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Finance.EquityReg', verbose_name='权益类登记'),
        ),
    ]
