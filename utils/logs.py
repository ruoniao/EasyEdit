# -*-coding:utf-8 -*-
__author__ = "ruoniao"
__date__ = "2018/1/25 9:20"
from datetime import datetime
from apps.users.models import UserLoginLog, UserOperateLog
from apps.document.models import DocumentLog


def write_login_logs(username, is_password, login_time=datetime.now(), is_active="Y"):
    login_logs = UserLoginLog(username=username, is_password=is_password, login_time=login_time)
    login_logs.save()
    return True


def write_operate_logs(username, operate, time=datetime.now()):
    log = UserOperateLog(username=username, operate=operate, time=time)
    log.save()
    return True


def write_document_log(doc_id, username, title, operate, edit_time=datetime.now()):
    log = DocumentLog(doc_id=doc_id, username=username, title=title, operate=operate, edit_time=edit_time)
    log.save()
