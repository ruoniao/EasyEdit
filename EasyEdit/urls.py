"""EasyEdit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from apps.users.views import RegisterView, LoginView, LogoutView
from apps.document.views import DocumenView, CreateDocumentView, LogsView, DocumentDeleteView, DocumentDetailView, \
    DocumentUpdateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', DocumenView.as_view()),
    url(r'^register/', RegisterView.as_view(), name="register"),
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^logout/', LogoutView.as_view(), name="logout"),
    url(r'^document/', DocumenView.as_view(), name="document"),
    url(r'^create/', CreateDocumentView.as_view(), name="createdoc"),
    url(r'^logs/', LogsView.as_view(), name="logs"),
    url(r'^deletedoc/(?P<doc_id>.+)$', DocumentDeleteView.as_view(), name="delete"),
    url(r'^detaildoc/(?P<doc_id>.+)$', DocumentDetailView.as_view(), name="detail"),
    url(r'^updatedoc/(?P<doc_id>.+)$', DocumentUpdateView.as_view(), name="update")
]
