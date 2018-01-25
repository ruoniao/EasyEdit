from django.contrib.auth.models import AbstractUser
from django.db import models
from mongoengine import *
from EasyEdit.settings import MONGO_HOST, MONGO_PORT

connect('EasyEdit', host=MONGO_HOST, port=MONGO_PORT)
# Create your models here.
active_status = {
    "N": "未激活",
    "Y": "激活",
}

is_password = {
    "Y": "正确",
    "N": "错误"
}


class UserProfile(AbstractUser):
    # username = models.CharField(max_length=50,verbose_name="用户名")
    # password = models.CharField(max_length=100,verbose_name="用户密码")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name


class UserLoginLog(Document):
    username = StringField(required=True)
    is_password = StringField(choices=is_password, required=True)
    login_time = DateTimeField(required=True)
    is_active = StringField(choices=active_status)


class MongoUser(Document):
    username = StringField(required=True, primary_key=True)
    password = StringField(required=True)


class UserOperateLog(Document):
    username = StringField(required=True, primary_key=True)
    operate = StringField(required=True)
    time = DateTimeField()
