import os

from django.core.management.base import NoArgsCommand
from django.conf import settings

from template_graph.graph import get_graph_json


class Command(NoArgsCommand):
    help = "Presaves a template graph to TEMPLATE_GRAPH_PATH"

    def handle_noargs(self, **options):
        path = getattr(settings, 'TEMPLATE_GRAPH_PATH', None)
        if path is not None:
            with open(os.path.join(path, 'template_graph.json'), 'w') as f:
                f.write(get_graph_json())
        else:
            print ('You must configure TEMPLATE_GRAPH_PATH if you want to '
                'save template graph JSON files for faster rendering. '
                'You likely want to add this file to .gitignore or similar '
                'as well. It will be named template_graph.json')
