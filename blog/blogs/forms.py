# -*- coding: utf-8 -*-

from django import forms

class RegisterFrom(forms.Form):
    # 邮箱
    email = forms.EmailField(required=True, error_messages={'invalid': '请填写正确的邮箱地址'})
    # 密码
    password = forms.CharField(required=True, min_length=6, error_messages={'invalid': '密码不能少于6位'})

    rePassword = forms.CharField(required=True, min_length=6,error_messages={'invalid': '密码不能少于6位'})

class LoginFrom(forms.Form):

    email = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=6)
