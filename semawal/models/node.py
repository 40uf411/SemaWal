import uuid
import time
import threading
# import the thread pool executor
from concurrent.futures import ThreadPoolExecutor
# Generate node model
class Node:
    # static variable of index type
    EDGE_TO_NODES = 0
    NODE_TO_EDGES = 1 
    # private variables
    _id = None
    _name = None
    _description = None
    _attributes = None
    _type = None
    _parent = None
    _children = None
    _compiled_edge_nodes_index = None
    _compiled_node_edges_index= None
    _num_workers = None
    # magic methods
    def __init__(self, name, description, type, attributes, parent = None, num_workers = 4) -> None:
        """Generate a node object.
        Args:
            name ([str]): Name of the node.
            description ([str]): Description of the node.
            attributes ([dict]): Attributes of the node.
            parent ([Node], optional): Parent node. Defaults to None.
        """
        self._id = str(uuid.uuid4())
        self._name = name if isinstance(name, str) else ''
        self._description = description if isinstance(description, str) else ''
        self._attributes = attributes if isinstance(attributes, dict) else {}
        self._type = type if isinstance(type, str) else 'regular'
        self._parent = parent
        self._children = []
        self._compiled_edge_nodes_index = {}
        self._compiled_node_edges_index = {}
        self._num_workers = num_workers if isinstance(num_workers, int) else 4
        self._tmp = {
            "key": "",
            "power": 1,
            "allow": True,
            "props": {}
        }

    def __str__(self):
        """String representation of the node.
        Returns: [str]
        """
        return "%:%" % (self._id, self._name)
    def __repr__(self):
        """String representation of the node.
        Returns: [str]
        """
        return self._str__()
    def __setattr__(self, name, value):
        """Set the node attribute.
        Args:
            name ([str]): Attribute name.
            value ([any]): Attribute value.
        Returns: [bool]
        """
        return False
    def __delattr__(self, name):
        """Drop the node attribute.
        Args:
            name ([str]): Attribute key.
        Returns: [bool]
        """
        return False

    # Checkers
    def is_parent (self, node) -> bool:
        """check is a node appears in the node parent of parent
        Args:
            node ([type]): Node to check.
        Returns:
            bool: True if the node is a parent.
        """
        if self._parent is None:
            return False
        if self._parent == node:
            return True
        return self._parent.is_parent(node)

    # Getters
    def get_id(self) -> str:
        """Get the node id.
        Returns:
            str: Node id.
        """
        return self._id
    def get_name(self) -> str:
        """Get the node name.
        Returns:
            str: Node name.
        """
        return self._name
    def get_description(self) -> str:
        """Get the node description.
        Returns:
            str: Node description.
        """
        return self._description
    def get_attributes(self) -> dict:
        """Get the node attributes.
        Returns:
            dict: Node attributes.
        """
        return self._attributes
    def get_attribute(self, key) -> any:
        """Get the node attribute.
        Args:
            key ([str]): Attribute key.
        Returns:
            dict: Node attribute.
        """
        return self._attributes[key] if key in self._attributes else None
    def get_type(self) -> str:
        """Get the node type.
        Returns:
            str: Node type.
        """
        return self._type
    def get_parent(self) -> any:
        """Get the node parent.
        Returns:
            Node: Node parent.
        """
        return self.__parent
    def get_root(self) -> any:
        """Get the root node.
        Returns:
            Node: Root node.
        """
        return self if self._parent is None else self._parent.get_root()
    def get_children(self) -> list:
        """Get the node children.
        Returns:
            list: Node children.
        """
        return self._children
    def get_edges(self, index=0) -> dict:
        """Get the node edges.
        Returns:
            dict: Node edges.
        """
        if index == 0:
            return self._compiled_edge_nodes_index
        else:
            return self._compiled_node_edges_index
    def get_num_workers(self) -> int:
        """Get the node number of workers.
        Returns:
            int: Node number of workers.
        """
        return self._num_workers

    # Setters
    def set_name(self, name: str) -> None:
        """Set the node name.
        Args:
            name ([str]): Name of the node.
        """
        self._name = name
    def set_description(self, description: str) -> None:
        """Set the node description.
        Args:
            description ([str]): Description of the node.
        """
        self._description = description
    def set_attributes(self, attributes: dict) -> None:
        """Set the node attributes.
        Args:
            attributes ([dict]): Attributes of the node.
        """
        self._attributes = attributes
    def set_attribute(self, key, value) -> None:
        """Set the node attribute.
        Args:
            key ([str]): Attribute key.
            value ([any]): Attribute value.
        """
        self._attributes[key] = value
    def set_type(self, type) -> None:
        """Set the node type.
        Args:
            type ([str]): Type of the node.
        """
        self._type = type if type in ['root', 'leaf', 'regular'] else 'regular'
        if self._type == 'root':
            self._parent = None
        elif self._type == 'leaf':
            for child in self._children:
                child.drop_parent()
            self._children = []
    def set_parent(self, parent) -> None:
        """Set the node parent.
        Args:
            parent ([Node]): Parent node.
        """
        if parent is None or not isinstance(parent, Node):
            return
        # Check if adding the parent is not a circular reference
        if self._type == 'root' or parent.get_type() == 'leaf' or parent.is_parent(self):
            return
        self._parent = parent
        # Add the node to the parent children
        self._parent.add_child(self)
    def set_num_workers(self, num_workers: int) -> None:
        """Set the node number of workers.
        Args:
            num_workers ([int]): Number of workers.
        """
        self._num_workers = num_workers
    # Adders
    def add_child(self, child) -> None:
        """Add a child to the node.
        Args:
            child ([Node]): Child node.
        """
        if child is None or not isinstance(child, Node):
            return
        self._children.append(child)
    def add_edge(self, key: str, node, power: int = 1, allow: bool = True, props: dict = {}) -> None:
        """Add a edge to the node.
        Args:
            key ([str]): EDGE key.
            node ([Node]): EDGE node.
            power ([int], optional): EDGE power. Defaults to 1.
            allow ([bool], optional): EDGE allow. Defaults to True.
            props ([dict], optional): EDGE properties. Defaults to {}.
        """
        if node is None or not isinstance(node, Node):
            return
        if key in self._edges:
            if node.get_id() not in self._edges[key].keys():
                self._edges[key][node.get_id()] = {
                    'power': power,
                    'allow': allow,
                    'props': props,
                    'node': node
                }
        else:
            self._edges[key] = {
                node.get_id(): {
                    'power': power,
                    'allow': allow,
                    'props': props,
                    'node': node
                }
            }
        self._tmp = {
            "power": power,
            "allow": allow,
            "props": props,
            'node': node
        }
    def and_with(self, node) -> None:
        """Add a edge to the node (this function uses the add_edge method).
        Args:
            node ([Node]): EDGE node.
        """
        self.add_edge(self._tmp['key'], node, self._tmp['power'], self._tmp['allow'], self._tmp['props'])

    # Droppers
    def drop_child(self, child) -> None:
        """Drop a child from the node.
        Args:
            child ([Node]): Child node.
        """
        self._children.remove(child)
    def drop_attribute(self, key: str) -> None:
        """Drop the node attribute.
        Args:
            key ([str]): Attribute key.
        """
        if key in self._attributes:
            del self._attributes[key]
    def drop_edge(self, key: str, node) -> None:
        """Drop the node edge.
        Args:
            key ([str]): EDGE key.
        """
        if key in self._edges and node.get_id() in self._edges[key]:
            self._edges[key].remove(node.get_id())
    def drop_parent(self) -> None:
        """Drop the node parent.
        """
        self._parent = None
        self._parent.drop_child(self)

    # recetters
    def reset(self, full_reset = False) -> None:
        """Reset the node to default values.
        """
        if full_reset:
            self._name = ""
            self._description = ""
            self._type = "regular"
            self._attributes = {}
        self._parent = None
        self._children = []
        self._edges = {}
        self._compiled_edge_nodes_index = {}
        self._compiled_node_edges_index = {}
        self._num_workers = 4
        self._tmp = {
            "key": "",
            "power": 1,
            "allow": True,
            "props": {}
        }

    # Commit changes and generat static indexes
    def commit(self) -> None:
        """Commit the node changes.
        """
        tmp_edges = self.get_parent.get_edges() if self.get_parent() is not None else {}
        # loop over the edges
        for edge_name, edges in self._edges:
            for node_id, edge in edges.items():
                # check if the edge with the node is in the parent edges
                if edge_name not in tmp_edges.keys() or node_id not in tmp_edges[edge_name]:
                    if edge_name not in tmp_edges.keys():
                        tmp_edges[edge_name] = {
                            node_id: edge
                        }
                    else:
                        # if not, add the edge
                        tmp_edges[edge_name][node_id] = edge
                elif edge['power'] > tmp_edges[edge_name][node_id]['power']:
                    # if so, replace the parent edge with the current edge
                    tmp_edges[edge_name][node_id] = edge
        # set the compiled edges
        self._compiled_edge_nodes_index = tmp_edges
        # compile the edges index
        self._compiled_node_edges_index = {}
        for edge_name, edges in self._compiled_edge_nodes_index.items():
            for node_id, edge in edges.items():
                if node_id in self._compiled_node_edges_index:
                    self._compiled_node_edges_index[node_id][edge_name] = edge
                else:                    
                    self._compiled_node_edges_index[node_id] = {
                        edge_name: edge
                    }
        # notify the children in a thread pool
        pool = ThreadPoolExecutor(self._num_workers)
        for child in self._children:
            pool.submit(child.commit)