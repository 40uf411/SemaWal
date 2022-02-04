import copy
import uuid
from semawal.models.node import Node
# Generate cluster of nodes model
class Cluster:
    def __init__(self, name, description) -> None:
        """Generate a cluster.
        Args:
            name ([str]): Name of the cluster.
            description ([str]): Description of the cluster.
        """
        self._id = str(uuid.uuid4())
        self._name = name
        self._description = description
        self._nodes = {}
        self._edge_source_index = {}
        self._edge_target_index = {}
        self._node_type_index = {}
    def __str__(self) -> str:
        """String representation of the cluster.
        Returns: [str]
        """
        return "%:%" % (self._id, self._name)
    def __repr__(self) -> str:
        """String representation of the cluster.
        Returns: [str]
        """
        return self._str__()
    def __setattr__(self, name, value):
        """Set the cluster attribute.
        Args:
            name ([str]): Attribute name.
            value ([any]): Attribute value.
        Returns: [bool]
        """
        # check is the attribute is private
        if not name.startswith('_'):
            return False
        # set the attribute
        self.__dict__[name] = value
    def __delattr__(self, name):
        """Drop the cluster attribute.
        Args:
            name ([str]): Attribute key.
        Returns: [bool]
        """
        # check is the attribute is private
        if not name.startswith('_'):
            return False
        # drop the attribute
        del self.__dict__[name]
    def __iter__(self)-> any:
        """Iterate over the cluster.
        Returns: [Iterator]
        """
        return iter(self._nodes)
    def __getitem__(self, key)-> Node|None:
        """Get the node by key.
        Args:
            key ([str]): Node key.
        Returns: [Node]
        """
        return self._nodes[key]
    def __len__(self) -> int:
        """Get the number of nodes.
        Returns: [int]
        """
        return len(self._nodes)

    # Getters
    def get_id(self) -> str:
        """Get the cluster id.
        Returns: [str]
        """
        return copy.deepcopy(self._id)
    def get_name(self) -> str:
        """Get the node name.
        Returns:
            str: Node name.
        """
        return copy.deepcopy(self._name)
    def get_description(self) -> str:
        """Get the node description.
        Returns:
            str: Node description.
        """
        return copy.deepcopy(self._description)
    def get_nodes(self) -> dict:
        """Get the nodes.
        Returns:
            dict: Nodes.
        """
        return copy.deepcopy(self._nodes)
    def get_node(self, key: str) -> Node|None:
        """Get the node by key.
        Args:
            key ([str]): Node key.
        Returns: [Node]
        """
        return self._nodes[key] if key in self._nodes else None
    def get_edge_source_index(self) -> dict:
        """Get the edge source index.
        Returns:
            dict: Edge source index.
        """
        return copy.deepcopy(self._edge_source_index)
    def get_edge_target_index(self) -> dict:
        """Get the edge target index.
        Returns:
            dict: Edge target index.
        """
        return copy.deepcopy(self._edge_target_index)
    def get_node_type_index(self) -> dict:
        """Get the node type index.
        Returns:
            dict: Node type index.
        """
        return copy.deepcopy(self._node_type_index)

    # Setters
    def set_name(self, name: str) -> bool:
        """Set the node name.
        Args:
            name ([str]): Node name.
        Returns: [bool]
        """
        self._name = name
        return True
    def set_description(self, description: str) -> bool:
        """Set the node description.
        Args:
            description ([str]): Node description.
        Returns: [bool]
        """
        self._description = description
        return True

    # Adders
    def add_node(self, node: Node) -> bool:
        """Add a node.
        Args:
            node ([Node]): Node to add.
        Returns: [bool]
        """
        if node.get_id() in self._nodes:
            return False
        self._nodes[node.get_id()] = node
        return True
    def add_nodes(self, nodes: list) -> bool:
        """Add a list of nodes.
        Args:
            nodes ([Node]): List of nodes to add.
        Returns: [bool]
        """
        for node in nodes:
            self.add_node(node)
        return True

    # Dropers
    def drop_node(self, node_id: str) -> bool:
        """Remove a node.
        Args:
            node_id ([str]): Node id.
        Returns: [bool]
        """
        if node_id in self._nodes:
            del self._nodes[node_id]
            return True
        return False

    # Resetter
    def reset(self, full_reset = False) -> bool:
        """Reset the cluster.
        Returns: [bool]
        """
        if full_reset:
            self._name = ""
            self._description = ""
        self._nodes = {}
        self._edge_source_index = {}
        self._edge_target_index = {}
        return True

    # Commit changes and generat static indexes
    def commit(self) -> None:
        """Commit changes.
        Returns: [None]
        """
        self._edge_source_index = {}
        self._edge_target_index = {}
        for node in self._nodes.values():
            for key, edge in node.get_edges().items():
                if key not in self._edge_source_index:
                    self._edge_source_index[key] = []
                self._edge_source_index[key].append(node)
                if key not in self._edge_target_index:
                    self._edge_target_index[key] = []
                for node_id, values in edge.items():
                    if values['node'] not in self._edge_target_index[key]:
                        self._edge_target_index[key].append(values['node'])

if __name__ == "__main__":
    # create a node "a" with type root and no parent
    node_a = Node(
    name="A",
    description="A node",
    type="root",
    attributes = {"a"
        "key": "value"
    },
    parent = None,
    num_workers = 4)
    # create a node "b" with type regular and no parent
    node_b = Node(
    name="B",
    description="B node",
    type="regular",
    attributes = {
        "key": "value"
    },
    parent = None,
    num_workers = 4)
    # create a node "c" with type regular and no parent
    node_c = Node(
    name="C",
    description="C node",
    type="regular",
    attributes = {
        "key": "value"
    },
    parent = node_b,
    num_workers = 4)
    # create a node "d" with type leaf and parent "a"
    node_d = Node(
    name="D",
    description="D node",
    type="leaf",
    attributes = {
        "key": "value"
    },
    parent = node_c,
    num_workers = 4)
    node_d.add_edge("edge_c", node_c, 1, True, {"key": "value"})
    node_d.commit()
    # create a node "e" with type leaf and no parent
    node_e = Node(
    name="E",
    description="E node",
    type="leaf",
    attributes = {
        "key": "value"
    },
    parent = None,
    num_workers = 4)
    # add a edge from "a" to "e"
    node_a.add_edge("edge_a", node_e, 1, True, {"key": "value"})
    node_a.commit()
    # create a cluster 
    cluster = Cluster(
        name="cluster_name",
        description="cluster_description")
    # add nodes to cluster
    cluster.add_nodes([node_a, node_b, node_c, node_d, node_e])
    # commit changes
    cluster.commit()
    print(node_d.get_root())