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
        self.__id = str(uuid.uuid4())
        self.__name = name
        self.__description = description
        self.__nodes = {}
        self.__edge_source_index = {}
        self.__edge_target_index = {}
        self.__node_type_index = {}
    def __str__(self) -> str:
        """String representation of the node.
        Returns: [str]
        """
        return "%:%" % (self.__id, self.__name)
    def __repr__(self) -> str:
        """String representation of the node.
        Returns: [str]
        """
        return self.__str__()
    def __setattr__(self, name, value) -> bool:
        """Set the node attribute.
        Args:
            name ([str]): Attribute name.
            value ([any]): Attribute value.
        Returns: [bool]
        """
        return False
    def __delattr__(self, name) -> bool:
        """Drop the node attribute.
        Args:
            name ([str]): Attribute key.
        Returns: [bool]
        """
        return False
    def __iter__(self)-> any:
        """Iterate over the nodes.
        Returns: [Iterator]
        """
        return iter(self.__nodes)
    def __getitem__(self, key)-> Node|None:
        """Get the node by key.
        Args:
            key ([str]): Node key.
        Returns: [Node]
        """
        return self.__nodes[key]
    def __len__(self) -> int:
        """Get the number of nodes.
        Returns: [int]
        """
        return len(self.__nodes)

    # Getters
    def get_id(self) -> str:
        """Get the cluster id.
        Returns: [str]
        """
        return self.__id
    def get_name(self) -> str:
        """Get the node name.
        Returns:
            str: Node name.
        """
        return self.__name
    def get_description(self) -> str:
        """Get the node description.
        Returns:
            str: Node description.
        """
        return self.__description
    def get_nodes(self) -> dict:
        """Get the nodes.
        Returns:
            dict: Nodes.
        """
        return self.__nodes
    def get_node(self, key: str) -> Node|None:
        """Get the node by key.
        Args:
            key ([str]): Node key.
        Returns: [Node]
        """
        return self.__nodes[key] if key in self.__nodes else None
    def get_edge_source_index(self) -> dict:
        """Get the edge source index.
        Returns:
            dict: Edge source index.
        """
        return self.__edge_source_index
    def get_edge_target_index(self) -> dict:
        """Get the edge target index.
        Returns:
            dict: Edge target index.
        """
        return self.__edge_target_index
    def get_node_type_index(self) -> dict:
        """Get the node type index.
        Returns:
            dict: Node type index.
        """
        return self.__node_type_index

    # Setters
    def set_name(self, name: str) -> bool:
        """Set the node name.
        Args:
            name ([str]): Node name.
        Returns: [bool]
        """
        self.__name = name
        return True
    def set_description(self, description: str) -> bool:
        """Set the node description.
        Args:
            description ([str]): Node description.
        Returns: [bool]
        """
        self.__description = description
        return True

    # Adders
    def add_node(self, node: Node) -> bool:
        """Add a node.
        Args:
            node ([Node]): Node to add.
        Returns: [bool]
        """
        if node.get_id() in self.__nodes:
            return False
        self.__nodes[node.get_id()] = node
        return True

    # Dropers
    def drop_node(self, node_id: str) -> bool:
        """Remove a node.
        Args:
            node_id ([str]): Node id.
        Returns: [bool]
        """
        if node_id in self.__nodes:
            del self.__nodes[node_id]
            return True
        return False

    # Resetter
    def reset(self, full_reset = False) -> bool:
        """Reset the cluster.
        Returns: [bool]
        """
        if full_reset:
            self.__name = ""
            self.__description = ""
        self.__nodes = {}
        self.__edge_source_index = {}
        self.__edge_target_index = {}
        return True

    # Commit changes and generat static indexes
    def commit(self) -> None:
        """Commit changes.
        Returns: [None]
        """
        self.__edge_source_index = {}
        self.__edge_target_index = {}
        for node in self.__nodes.values():
            for edge in node.get_edges():
                if edge.get_source() not in self.__edge_source_index:
                    self.__edge_source_index[edge.get_source()] = []
                self.__edge_source_index[edge.get_source()].append(edge)
                if edge.get_target() not in self.__edge_target_index:
                    self.__edge_target_index[edge.get_target()] = []
                self.__edge_target_index[edge.get_target()].append(edge)
