import uuid
from semawal.models import Cluster
from semawal.models import Node
from semawal.tools.resolvers.term import Term
# an object that will allow us to execute queries against a cluster.
# the cluster is represented as a Cluster object, which contains a dictionary of Node objects.
# the Node objects contain a dictionary edges.
# Examples:
""" 
    - Query().on_cluster(cluster)
        .with_node_filter(lambda node, index: node.name == 'node_name')
        .with_edge_filter(lambda edge, index: edge.name == 'edge_name')
        .fetch_paths(from_note='node_name', to_node='node_name', max_depth=15)
        .run_on(network)
"""
class Query:
    def __init__(self) -> None:
        """Initialize the query object.
        Args:
            cluster ([Cluster]): Cluster object.
        """
        self.__cluster = None
        self.__node_filter = None
        self.__edge_filter = None
        self.__query_id = str(uuid.uuid4())

    # Methods
    def on_cluster(self, cluster: Cluster) -> any:
        """Set the cluster.
        Args:
            cluster ([Cluster]): Cluster object.
        Returns: Query
        """
        self.__cluster = cluster
        return self
    def with_node_filter(self, node_filter: callable) -> any:
        """Set the node filter.
        Args:
            node_filter (callable): Node filter.
        Returns: Query
        """
        self.__node_filter = node_filter
        return self
    def with_edge_filter(self, edge_filter: callable) -> any:
        """Set the edge filter.
        Args:
            edge_filter (callable): Edge filter.
        Returns: Query
        """
        self.__edge_filter = edge_filter
        return self
    def fetch_paths(self, from_node: Node, to_node: Node, max_depth: int) -> any:
        """Fetch paths.
        Args:
            from_ (Node): From node name.
            to (Node): To node name.
            max_depth (int): Maximal depth.
        Returns: Query
        """
        self.__function = "fetch_paths"
        self.__from = from_node
        self.__to = to_node
        self.__max_depth = max_depth
        return self
    def fetch_nodes(self) -> any:
        """Fetch nodes.
        Returns: Query
        """
        self.__function = "fetch_nodes"
        return self
    def fetch_nodes_accessible(self, to_node: Node) -> any:
        """Fetch accessible nodes.
        Args:
            to_node (Node): To node.
        Returns: Query
        """
        self.__function = "fetch_nodes_accessible"
        self.__to = to_node
        return self
    def run_on(self, network: dict) -> list:
        """Run on.
        Args:
            network (dict): Network.
        Returns: list
        """
        # get the paths
        paths = self.__get_paths(network)
        # filter the paths
        paths = self.__filter_paths(paths)
        # return the paths
        return paths