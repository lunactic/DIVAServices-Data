from django.conf.urls import url
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings


from uploader.views import uploader
from divaGui.views.addcollection import addcollection
from divaGui.views.CollectionView import CollectionView
from divaGui.views.AboutView import AboutView
from divaGui.views.ContactTemplateView import ContactTemplateView
from divaGui.views.CollectionsView import CollectionsView
from divaGui.views.MethodView import MethodView
from divaGui.views.MethodsView import MethodsView
from divaGui.views.Tryouts import  TryoutsTemplateView
from divaGui.views.DeleteCollectionView import DeleteCollectionView
from divaGui.views.HighlighterView import HighlighterView




urlpatterns = [
    url(r'^admin/$', admin.site.urls),
    url(r'^$', CollectionsView.as_view()),
    url(r'^about/$', AboutView.as_view()),
    url(r'^AdminAdminDelete/$', DeleteCollectionView.as_view()),
    url(r'^practise/$', TryoutsTemplateView.as_view()),
    url(r'^addnewcollection/(?P<url>[\w\W]*)$', addcollection),
    url(r'^contact/$', ContactTemplateView.as_view()),
    url(r'^collections/(?P<something>[\w\W]*)$', CollectionsView.as_view()),
    url(r'^methods/(?P<something>[\w\W]*)$', MethodsView.as_view()),
    url(r'^method/(?P<url>[\w\W]*)$', MethodView.as_view()),
    url(r'^collection/(?P<url>[\w\W]*)$', CollectionView.as_view()),
    url(r'^highlighter/(?P<url>[\w\W]*)$', HighlighterView.as_view()),
    url(r'^uploader/(?P<url>[\w\W]*)$', uploader, name='imageupload'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)