from django.core.management.base import NoArgsCommand

from template_graph.graph import get_digraph


class Command(NoArgsCommand):
    help = "Saves the directed graph of templates to a DOT file"

    def handle_noargs(self, **options):
        with open('templates.dot', 'w') as f:
            f.write(get_digraph())
