from django.db import models
from mongoengine import *
from EasyEdit.settings import MONGO_HOST, MONGO_PORT

connect('EasyEdit', host=MONGO_HOST, port=MONGO_PORT)


# Create your models here.



class EditDocument(Document):
    title = StringField(required=True)
    username = StringField(required=True)
    create_time = DateTimeField()
    content = StringField(required=True)


class DocumentLog(Document):
    doc_id = StringField(required=True)
    title = StringField(required=True)
    username = StringField(required=True)
    edit_time = DateTimeField(required=True)
    operate = StringField(required=True)
