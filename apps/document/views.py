from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime
from django.views import View
from utils.mixin_utils import LoginRequiredMixin
from .models import EditDocument, DocumentLog
from utils.logs import write_document_log
from bson import ObjectId
from collections import namedtuple


class DocumenView(LoginRequiredMixin, View):
    def get(self, requset):
        all_document = EditDocument.objects.all().order_by('-create_time')
        documents_msg = []
        for document in all_document:
            doc_log = DocumentLog.objects.filter(doc_id=document.id).order_by('-edit_time').first()

            id = document.id
            title = document.title
            username = document.username
            content = document.content
            if doc_log:
                last_operater, last_time = doc_log.username, doc_log.edit_time
            else:
                last_operater, last_time = "增加", document.create_time
            document_msg = namedtuple('document_msg',
                                      ['id', 'title', 'username', 'content', 'last_operater', 'last_time'])
            doc_msg = document_msg(id=id, title=title, username=username, content=content, last_operater=last_operater,
                                   last_time=last_time)

            documents_msg.append(doc_msg)

        length = len(documents_msg)
        return render(requset, "document.html", {"documents_msg": documents_msg, "length": length})


class CreateDocumentView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "document_create.html", {"username": request.user.username})

    def post(self, request):
        username = request.user.username
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        create_time = datetime.now()
        my_document = EditDocument(username=username, title=title, content=content, create_time=create_time)
        my_document.save()

        write_document_log(doc_id=str(my_document.id), username=username, title=title, operate="新增")
        return HttpResponseRedirect("/document/")


class DocumentDetailView(LoginRequiredMixin, View):
    def get(self, request, doc_id):
        doc = EditDocument.objects.filter(id=doc_id).first()
        log = DocumentLog.objects.filter(doc_id=doc_id).first()
        if log:
            last_time = log.edit_time
        else:
            last_time = doc.create_time
        if doc is None:
            return render(request, "detail.html", {"no_doc": "该文档已不存在"})
        return render(request, "detail.html", {"doc": doc, "last_time": last_time})


class DocumentUpdateView(LoginRequiredMixin, View):
    def get(self, request, doc_id):
        doc = EditDocument.objects.filter(id=doc_id).first()
        last_time = DocumentLog.objects.filter(doc_id=doc_id).first().edit_time
        return render(request, "update.html", {"doc": doc, "last_time": last_time})

    def post(self, request, doc_id):
        doc = EditDocument.objects.filter(id=doc_id).first()
        new_title = request.POST.get("title", "")
        new_content = request.POST.get("content", "")
        doc.update(title=new_title)
        doc.update(content=new_content)
        write_document_log(doc_id=doc_id, username=request.user.username, operate="修改", title=new_title)
        return HttpResponseRedirect("/document/")


class DocumentDeleteView(LoginRequiredMixin, View):
    def get(self, request, doc_id):
        doc = EditDocument.objects.filter(id=doc_id).first()
        title = doc.title
        doc.delete()
        write_document_log(doc_id=doc_id, username=request.user.username, operate="删除", title=title)
        return HttpResponseRedirect("/document/")


class LogsView(LoginRequiredMixin, View):
    def get(self, request):
        doc_logs = DocumentLog.objects.all().order_by("edit_time")

        length = len(doc_logs)
        return render(request, "logs.html", {"doc_logs": doc_logs, "length": length})
