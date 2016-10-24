# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-17 03:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0026_auto_20161014_1611'),
    ]

    operations = [
        migrations.CreateModel(
            name='BatchImport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=50, null=True, verbose_name='导入名称')),
                ('UploadFile', models.FileField(upload_to='./upload/')),
                ('UploadTime', models.DateTimeField(null=True, verbose_name='上传时间')),
            ],
            options={
                'ordering': ['UploadTime'],
                'verbose_name': '数据导入',
                'verbose_name_plural': '数据导入',
            },
        ),
        migrations.AlterField(
            model_name='equity',
            name='Type',
            field=models.CharField(blank=True, choices=[('1', '上海'), ('2', '深圳'), ('3', '基金'), ('3', '自定义')], max_length=1, null=True, verbose_name='类型'),
        ),
    ]