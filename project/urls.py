"""muypicky URL Configuration

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

from django.conf.urls.static import static
from django.conf import settings

from divaGui.views import ContactTemplateView, CollectionsView, DeleteCollectionView, CollectionView, MethodsView, TryoutsTemplateView, addcollection, MethodView
from uploader.views import uploader


urlpatterns = [
    url(r'^admin/$', admin.site.urls),
    url(r'^$', CollectionsView.as_view()),
    url(r'^practise/$', TryoutsTemplateView.as_view()),
    url(r'^addnewcollection/(?P<url>[\w\W]*)$', addcollection),
    url(r'^deletecollection/$', DeleteCollectionView.as_view()),
    url(r'^contact/$', ContactTemplateView.as_view()),
    url(r'^collections/(?P<something>[\w\W]*)$', CollectionsView.as_view()),
    url(r'^methods/(?P<something>[\w\W]*)$', MethodsView.as_view()),
    url(r'^method/(?P<url>[\w\W]*)$', MethodView.as_view()),
    url(r'^collection/(?P<url>[\w\W]*)$', CollectionView.as_view()),
    url(r'^uploader/(?P<url>[\w\W]*)$', uploader, name='imageupload'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
