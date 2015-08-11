#-*- coding=utf-8 -*-
from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='手机号码:',max_length = 20)
    SMS_code = forms.CharField(label='短信验证码:', max_length = 20)
    password = forms.CharField(label='密码:',widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码:',widget=forms.PasswordInput())

