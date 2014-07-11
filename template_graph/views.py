from django.views.generic import TemplateView

from template_graph.node_tree import get_tree_json

class TemplateGraphView(TemplateView):
    template_name = 'template_graph/list.html'

    def get_context_data(self, **kwargs):
        ctx = super(TemplateGraphView, self).get_context_data(**kwargs)
        ctx['tree'] = self.get_tree()
        return ctx

    def get_tree(self):
        return get_tree_json()
