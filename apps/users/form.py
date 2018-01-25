# -*-coding:utf-8 -*-
__author__ = "ruoniao"
__date__ = "2018/1/16 15:33"
from django import forms
from .models import UserProfile


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, min_length=3)
    password = forms.CharField(required=True, min_length=6)


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=3)
    password = forms.CharField(required=True, min_length=6)


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["username"]
