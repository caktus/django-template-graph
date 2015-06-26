import os

from django.conf import settings

from template_graph.graph import get_graph_json
from template_graph.management.commands.template_graph_gen import Command as GenCommand

graph_gen_command = GenCommand()


def fetch_or_create_tree_json():
    graph_path = getattr(settings, 'TEMPLATE_GRAPH_PATH', None)
    if graph_path is not None:
        filename = os.path.join(graph_path, 'template_graph.json')
        if not os.path.exists(filename):
            graph_gen_command.handle_noargs()
        with open(filename) as f:
            return f.read()
    else:
        return get_graph_json
