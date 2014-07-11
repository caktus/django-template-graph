import json

from django.views.generic import TemplateView


class TemplateGraphView(TemplateView):
    template_name = 'template_graph/list.html'

    def get_context_data(self, **kwargs):
        ctx = super(TemplateGraphView, self).get_context_data(**kwargs)
        ctx['tree'] = self.get_tree()
        return ctx

    def get_tree(self):
        return json.dumps([
            {
                'id': 1,
                'name': 'base.html',
                'includes': [],
                'children': [
                    {
                        'id': 2,
                        'name': 'example2.html',
                        'includes': [],
                        'children': [
                            {
                                'id': 4,
                                'name': 'example4.html',
                                'includes': [],
                                'children': [],
                            },
                            {
                                'id': 5,
                                'name': 'example5.html',
                                'includes': [],
                                'children': []
                            }
                        ]
                    },
                    {
                        'id': 3,
                        'name': 'example3.html',
                        'includes': [],
                        'children': []
                    }
                ]
            }
        ])
