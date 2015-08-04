import os
import json

from collections import defaultdict

from template_graph.line_stream import (get_template_line_stream,
    INCLUDE_TAG, EXTEND_TAG, BLOCK_TAG, NO_TAG)


class Graph(object):
    """
    Stores the overall graph, made of nodes with data about each template.

    Contains extends and includes relationships as lists of two-tuples
    """

    def __init__(self):
        self.node_reg = NodeRegistry()
        # lists two tuples of extends
        self.extend_edges = []
        # lists two tuples of includes
        self.include_edges = []
        # map of node id -> blocks that it defines
        self.blocks = defaultdict(list)
        # set of root nodes in extend hierarchies
        self.root_node_ids = set()
        # set of templates w/o extends or includes
        self.lone_node_ids = set()
        # map of node id -> information about each node
        self.nodes = {}
        # A string holding the Graphviz digraph of extends/includes
        self.digraph = ''
        # Initiate building of graph object
        self._process()

    def _process(self):
        connected_node_ids = set()
        possible_lone_node_ids = set()
        possible_root_ids = set()
        not_root_ids = set()
        extends = defaultdict(list)
        for line in get_template_line_stream():
            source = self.node_reg.get_or_create_node(line.source, line.path)
            if line.tag_type in set([INCLUDE_TAG, EXTEND_TAG]):
                target = self.node_reg.get_or_create_node(line.target, line.path)
                connected_node_ids.add(source.id)
                connected_node_ids.add(target.id)
                if line.tag_type == EXTEND_TAG:
                    possible_root_ids.add(target.id)
                    not_root_ids.add(source.id)
                    extends[target.id].append(source.id)
                    self.extend_edges.append((target.id, source.id))
                if line.tag_type == INCLUDE_TAG:
                    self.include_edges.append((source.id, target.id))
            if line.tag_type == BLOCK_TAG:
                self.blocks[source.id].append(line.target)
            if line.tag_type == NO_TAG:
                possible_lone_node_ids.add(source.id)
        self.lone_node_ids = possible_lone_node_ids - connected_node_ids
        self.root_node_ids = possible_root_ids - not_root_ids
        self.nodes = self._create_nodes()
        self.digraph = ''.join(self.digraph_gen())

    def _create_nodes(self):
        return dict([
            (node_id, node.as_dict())
            for node_id, node in self.node_reg._id_node_registry.iteritems()
        ])

    def digraph_gen(self):
        def node_name_finder(edge):
            return self.nodes[edge]['name']
        yield('digraph {')
        for edge in self.extend_edges:
            yield('    "{0}" -> "{1}"'.format(*map(node_name_finder, edge)))
        for edge in self.include_edges:
            yield('    "{0}" -> "{1}" [color=" 1.0 0.5 1.0"]'.format(
                *map(node_name_finder, edge)))
        yield('}')

    def as_dict(self):
        return {
            'nodes': self.nodes,
            'digraph': self.digraph,
            'lone_node_ids': list(self.lone_node_ids),
            'root_node_ids': list(self.root_node_ids),
            'include_edges': self.include_edges,
            'extend_edges': self.extend_edges,
            'blocks': self.blocks,
        }

    @property
    def as_json(self):
        return json.dumps(self.as_dict())


class NodeRegistry(object):
    """
    Acts as a factory to create nodes with unique id's per their filename and
    path and a lookup table for nodes by id once created.
    """

    def __init__(self):
        self._node_id = 0
        self._id_node_registry = {}
        self._filename_registry = {}

    def get_or_create_node(self, filename, path):
        key = ':'.join((filename, path))
        existing = self._filename_registry.get(key, None)
        if existing is not None:
            return existing
        else:
            new_node = Node(self._node_id, filename, path)
            self._id_node_registry[new_node.id] = new_node
            self._filename_registry[key] = new_node
            self._node_id += 1
            return new_node

    def get_node_by_id(self, id):
        return self._id_node_registry.get(id, None)

    def __iter__(self):
        for k_v_pair in self._id_node_registry.iteritems():
            yield k_v_pair


class Node(object):
    """
    Stores a unique id, filename, for each template as a node in the overall
    graph
    """

    def __init__(self, id, filename, path):
        self.id = id
        self.filename = filename
        self.path = path

    @property
    def name(self):
        if self.filename.startswith('variable:'):
            return self.filename
        else:
            return os.path.relpath(self.filename, self.path)

    @property
    def appname(self):
        try:
            app_name = os.path.split(self.name)[0]
        except IndexError:
            return 'Unknown?'
        else:
            return app_name if app_name else '/'

    def __str__(self):
        return str(self.as_dict())

    def as_dict(self):
        return {
            'id': self.id,
            'app': self.appname,
            'path': self.path,
            'filename': self.filename,
            'name': self.name,
        }


def get_graph_json():
    return Graph().as_json

def get_digraph():
    return ''.join(list(Graph().digraph_gen()))
