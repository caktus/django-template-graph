import json

from template_graph.line_stream import get_template_line_stream


class NodeRegistry(object):
    """
    Stores the aggregation of all Nodes. This is essentially a list of trees.
    The walk* methods yield each root node, which in turn have data for all of
    their children.

    To do this, mappings for filename->id and id->filename are kept as each
    node is added. Each line provided supplies a source and target node and
    both are updated if they exit, otherwise they are added. Each node is
    given a unique id for reference from other nodes

    The root_node_ids attribute stores the set of "root" nodes. These are base
    templates, but also "include" templates (templates that are only ever
    included but do not extend another.) These are not truly "root" nodes, but
    need to be returned in the aggregate so that they can be part of the
    output.
    """
    _max_val = 0

    def __init__(self):
        self.filename_id_registry = {}
        self.id_node_registry = {}
        self.root_node_ids = set([])

    def _get_or_create_node(self, line, attribute):
        """
        Fetch an existing node by filename or create one if it
        doesn't exist. Uses `attribute` to determine if the source
        or target filename should be used from the TemplateLine given
        as `line`
        """
        filename = getattr(line, attribute)
        node = self.filename_id_registry.get(filename, None)
        if node is None:
            node = Node(self.__class__._max_val, filename)
            self.__class__._max_val += 1
        return node

    def _get_or_create_source_node(self, line):
        return self._get_or_create_node(line, 'source')

    def _get_or_create_target_node(self, line):
        return self._get_or_create_node(line, 'target')

    def _update_registries(self, line, node, target):
        """
        Takes a template line, a source node and a target node
        and updates the internal mappings with updated nodes from
        the add method
        """
        self.filename_id_registry[line.source] = node
        self.filename_id_registry[line.target] = target
        self.id_node_registry[node.id] = node
        self.id_node_registry[target.id] = target

    def add(self, line):
        """
        Given a TemplateLine `line` from line_stream.get_template_line_stream,
        creates and/or updates existing nodes in the registry as needed
        """
        node = self._get_or_create_source_node(line)
        target = self._get_or_create_target_node(line)
        if line.tag_type == 'extends':
            node.parent = target.id
            target.children_ids.append(node.id)
            if node.id in self.root_node_ids:
                self.root_node_ids.remove(node.id)
            if target.parent is None:
                self.root_node_ids.add(target.id)
        if line.tag_type == 'include':
            node.includes.append(target.id)
            if node.parent is not None and node.id in self.root_node_ids:
                self.root_node_ids.remove(node.id)
            if target.parent is None:
                self.root_node_ids.add(target.id)
        self._update_registries(line, node, target)

    def fill_children(self, node):
        """
        Use children_ids of a given node to fill its children list with node
        objects. Vist each of these child nodes and fill their children list
        with nodes as well until leaf nodes are reached
        """
        for child_id in node.children_ids:
            child_node = self.id_node_registry[child_id]
            if child_node.children_ids != []:
                child_node = self.fill_children(child_node)
            node.children.append(child_node)
        return node

    def walk_nodes(self):
        """
        Walk the root nodes, fill their children with data and return them
        """
        for node_id in self.root_node_ids:
            # Calls fill_children for its side-effect, returns the altered node
            node = self.fill_children(self.id_node_registry[node_id])
            yield node

    def walk(self):
        """
        Walk each node in the tree and return a dictionary representation of
        each
        """
        return (node.as_dict() for node in self.walk_nodes())


class Node(object):
    """
    Stores the id, filename and associates for each node
    """

    def __init__(self, id, filename):
        self.id = id
        self.filename = filename
        self.parent = None
        self.children_ids = []
        self.children = []
        self.includes = []

    def as_dict(self):
        return {
            'id': self.id,
            'parent': self.parent,
            'includes': self.includes,
            'children': [c.as_dict() for c in self.children]
        }


def get_node_registry():
    """
    Creates a NodeRegistry and adds all nodes from the get_template_line_stream
    """
    registry = NodeRegistry()
    for line in get_template_line_stream():
        registry.add(line)
    return registry


# Returns a list of dictionaries of Node data
get_tree_data = lambda: get_node_registry().walk()
# Returns the tree data in JSON
get_tree_json = lambda: json.dumps(list(get_tree_data()))


if __name__ == '__main__':
    print get_tree_json()
