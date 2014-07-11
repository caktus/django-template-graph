from django.conf import settings
from django.conf.urls import patterns,  url

from .views import TemplateGraphView


urlpatterns = patterns('')

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^$', TemplateGraphView.as_view()),
    )
