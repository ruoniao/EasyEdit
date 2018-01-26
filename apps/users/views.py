from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime, timedelta, timedelta
import time
# Create your views here.
import pymongo

client = pymongo.MongoClient("127.0.0.1", 27017)

db = client.EasyEdit
from django.views import View

from apps.users.form import RegisterForm, LoginForm
from .models import UserProfile, MongoUser, UserLoginLog
from utils.logs import write_login_logs, write_operate_logs


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(username=username)
            if user.check_password(password):
                return user

        except Exception as e:

            return None


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("username", "")
            if UserProfile.objects.filter(username=user_name):
                return render(request, "register.html", {"msg": "用户已经存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.is_active = True
            user_profile.password = make_password(pass_word)
            mongo_user = MongoUser(username=user_name, password=user_profile.password)
            mongo_user.save()
            user_profile.save()
            write_operate_logs(username=user_name, operate="注册")
            return HttpResponseRedirect('/login/')
        else:
            return render(request, "register.html", {"register_form": register_form})


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login_form = LoginForm(request.POST)

        # 判断表单验证
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            # 在用户登录日志内,若在15分钟内登录错误次数超过3次不允许登录
            # 尝试取出最近的三次，并判断这三次是否全部密码输入错误和最后一次输错密码是在15分钟之内的冻结
            user_log = list(db.user_login_log.find({"username": "{}".format(username)}).sort("login_time")[:3])
            if len(user_log) >= 3:
                user_log1, user_log2, user_log3 = user_log
                if user_log1["is_password"] == "N" and user_log2["is_password"] == "N" and user_log3[
                    "is_password"] == "N" and user_log1["login_time"] >= (
                            datetime.now() - timedelta(hours=0, minutes=15, seconds=0)):
                    return render(request, "login.html", {"msg": "账号冻结,{}分钟后再试".format(str(
                            timedelta(hours=0, minutes=15, seconds=0) - (
                            datetime.now() - user_log1["login_time"])).split(
                            ":")[1])})
                else:
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        write_login_logs(username=username, is_password="Y")
                        return HttpResponseRedirect('/document/')
                    else:
                        write_login_logs(username=username, is_password="N")
                        return render(request, "login.html", {"msg": "用户名或密码错误"})
            else:
                # 判断密码是否正确
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/document/')
                else:
                    write_login_logs(username=username, is_password="N")
                    return render(request, "login.html", {"msg": "用户名或密码错误"})

        else:
            # 返回表单验证的错误信息
            return render(request, "login.html", {"login_form": login_form})


class LogoutView(View):
    def get(self, request):
        write_operate_logs(username=request.user.username, operate="登出", )
        logout(request)

        return HttpResponseRedirect('/login/')
