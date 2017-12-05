#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:沈中秋
# date:"2017-12-05,19:38"

from django.forms import Form, fields, widgets
from . import models


class QuestionnaireForm(Form):
    title = fields.CharField(required=True, error_messages={
        "required": "问题不能为空"
    },
                             widget=widgets.TextInput(attrs={"class": "form-control"}))

    cls = fields.ChoiceField(required=True, error_messages={
        "required": "班级不能为空"
    },
                             choices=models.ClassList.objects.values_list("id", "title"),
                             widget=widgets.Select(attrs={"class": "form-control","placeholder":"请选择班级"}))



