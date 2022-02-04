import uuid
from semawal.models import Cluster, Node
from semawal.tools.resolvers import cursor
from semawal.tools.resolvers.cursor import Cursor
# an object that will allow us to execute queries against a cluster.
# the cluster is represented as a Cluster object, which contains a dictionary of Node objects.
# the Node objects contain a dictionary edges.
# Examples:
""" 
    - Query().on_cluster(cluster)
        .with_node_filter(lambda node, index: node.name == 'node_name')
        .with_edge_filter(lambda edge, index: edge.name == 'edge_name')
        .set_max_depth(2)
        .set_limit(5)
        .fetch_paths(from_note='node_name', to_node='node_name', max_depth=15)
        .run()
"""
class Query:
    def __init__(self) -> None:
        """Initialize the query object.
        Args:
            cluster ([Cluster]): Cluster object.
        """
        self._cluster = None
        self._node_filter = None
        self._edge_filter = None
        self._max_depth = None
        self._limit = None
        self._function = None
        self._from = None
        self._to = None
        self._num_workers = None
        self._query_id = str(uuid.uuid4())

    # Methods
    def on_cluster(self, cluster: Cluster) -> any:
        """Set the cluster.
        Args:
            cluster ([Cluster]): Cluster object.
        Returns: Query
        """
        self._cluster = cluster
        return self
    def with_node_filter(self, node_filter: callable) -> any:
        """Set the node filter.
        Args:
            node_filter (callable): Node filter.
        Returns: Query
        """
        self._node_filter = node_filter
        return self
    def with_edge_filter(self, edge_filter: callable) -> any:
        """Set the edge filter.
        Args:
            edge_filter (callable): Edge filter.
        Returns: Query
        """
        self._edge_filter = edge_filter
        return self
    def set_max_depth(self, max_depth: int) -> any:
        """Set the max depth.
        Args:
            max_depth (int): Max depth.
        Returns: Query
        """
        self._max_depth = max_depth
        return self
    def set_limit(self, limit: int) -> any:
        """Set the limit of how many paths to get.
        Args:
            limit (int): Limit.
        Returns: Query
        """
        self._limit = limit
        return self
    def fetch_paths(self, from_node: Node, to_node: Node) -> any:
        """Fetch paths.
        Args:
            from_ (Node): From node name.
            to (Node): To node name.
            max_depth (int): Maximal depth.
        Returns: Query
        """
        self._function = "fetch_paths"
        self._from = from_node
        self._to = to_node
        return self
    def fetch_nodes(self) -> any:
        """Fetch nodes.
        Returns: Query
        """
        self._function = "fetch_nodes"
        return self
    def fetch_nodes_accessible(self, from_node: Node) -> any:
        """Fetch accessible nodes.
        Args:
            to_node (Node): To node.
        Returns: Query
        """
        self._function = "fetch_nodes_accessible"
        self._to = from_node
        return self
    def run(self, num_workers) -> Cursor:
        """Run a query.
        Args:
            network (dict): Network.
        Returns: list
        """
        # filter the nodes using the self._node_filter
        self._num_workers = num_workers
        # Switch case on the function
        if self._function == "fetch_paths":
            return self._fetch_paths()
        elif self._function == "fetch_nodes":
            return Cursor([node for node in self._cluster.get_nodes() if self._node_filter(node, 0)])
        elif self._function == "fetch_nodes_accessible":
            return self._fetch_nodes_accessible()
        else:
            raise Exception("Function not implemented.")

    # Private methods
    def _fetch_paths(self) -> Cursor:
        """Fetch paths.
        Returns: Cursor
        """
        # get the paths
        paths = self._get_paths(nodes, self._from, self._to, self._max_depth, self._limit)
        # create a cursor
        cursor = Cursor(paths)
        # return the cursor
        return cursor
    def _fetch_nodes_accessible(self) -> Cursor:
        """Fetch accessible nodes.
        Returns: Cursor
        """ 
        # get the accessible nodes
        accessible_nodes = self._get_accessible_nodes(nodes, self._to)
        # create a cursor
        cursor = Cursor(accessible_nodes)
        # return the cursor
        return cursor
