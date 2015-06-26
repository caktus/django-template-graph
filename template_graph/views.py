from django.conf import settings
from django.views.generic import TemplateView
from django.http import Http404

from template_graph.utils import fetch_or_create_tree_json


class TemplateGraphView(TemplateView):
    template_name = 'template_graph/list.html'

    def dispatch(self, *args, **kwargs):
        if not settings.DEBUG:
            raise Http404
        return super(TemplateGraphView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(TemplateGraphView, self).get_context_data(**kwargs)
        ctx['tree'] = fetch_or_create_tree_json()
        return ctx

