# -*- coding: utf-8 -*-
# @Time    : 2018/11/8 14:44
# @Author  : xinjie

from django import forms
from operation.models import UserAsk
import re

# class AnotherUserForm(forms.ModelForm):
#     # 继承之余还可以新增字段
#
#     # 是由哪个model转换的
#     class Meta:
#         model = UserAsk
#         # 我需要验证的字段
#         fields = ['name','mobile','course_name']


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # 手机号的正则表达式验证
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")