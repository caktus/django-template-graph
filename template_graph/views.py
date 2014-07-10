import json

from django.views.generic import TemplateView


class TemplateGraphView(TemplateView):
    template_name = 'template_graph/list.html'

    def get_context_data(self, **kwargs):
        ctx = super(TemplateGraphView, self).get_context_data(**kwargs)
        ctx['tree'] = self.get_tree()
        return ctx

    def get_tree(self):
        return json.dumps({
            1: {
                'id': 1,
                'parent': None,
                'file_path': '../templates/example1.html',
                'includes': [],
                'children': [
                    {
                        4: {
                            'id': 1,
                            'parent': None,
                            'file_path': '../templates/example2.html',
                            'includes': [],
                            'children': [],
                        },
                        5: {
                            'id': 1,
                            'parent': None,
                            'file_path': '../templates/example3.html',
                            'includes': [],
                            'children': []
                        }
                    }
                ]
            },
            2: {
                'id': 1,
                'parent': None,
                'file_path': '../templates/example.html',
                'includes': [],
                'children': []
            },
            3: {
                'id': 1,
                'parent': None,
                'file_path': '../templates/example.html',
                'includes': [],
                'children': [],
            }
        })
