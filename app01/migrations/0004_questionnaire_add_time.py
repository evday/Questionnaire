# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_questionnaire_take_part_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, default=2, verbose_name='创建时间'),
            preserve_default=False,
        ),
    ]
