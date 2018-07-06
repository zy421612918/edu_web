#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-5-26

from django import forms
from captcha.fields import CaptchaField
from models import UserProfile


class LoginForm(forms.Form):

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha= CaptchaField(error_messages={'invalid':'验证码错误'})


class ForgetForm(forms.Form):

    email = forms.EmailField(required=True)
    captcha= CaptchaField(error_messages={'invalid':'验证码错误'})



class ModifyPwdForm(forms.Form):

    password1 = forms.CharField(required=True, min_length=6)
    password2= forms.CharField(required=True, min_length=6)


class UploadImageForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['image']




