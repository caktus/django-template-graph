from django.conf.urls import patterns,  url

from .views import TemplateGraphView


urlpatterns = patterns('',
    url(r'^$', TemplateGraphView.as_view()),
)
