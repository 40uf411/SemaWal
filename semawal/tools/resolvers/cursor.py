import uuid
from semawal.models.cluster import Cluster, Node
# List of functions:
"""
- select all the paths between two Nodes while respecting the following criteria:
    - respecting the maximal depth.
    - respecting the given criteria on each Node (e.g. name, description, etc.).
    - respecting the given criteria on the edges between the Nodes.
    - the criteria on the edges can be a list of criteria, each of which will be evaluated on the edge with the corresponding depth.
- 
"""
class Cursor:
    def __init__(self, data: any) -> None:
        """ Initialize the cursor object.
        """
        self._data = data
    def __iter__(self) -> any:
        """ Iterate over the data.
        """
        return iter(self._data)

    # Methods
    def get_data(self) -> any:
        """ Get the data.
        """
        return self._data


    # def __init__(self, cluster: Cluster, node_filter: callable, edge_filter: callable, max_depth: int,limit: int, function: str, from_node: Node, to_node: Node, num_workers: int) -> None:
    #     """ Initialize the cursor object.
    #     """
    #     self._cluster = cluster
    #     self._node_filter = node_filter
    #     self._edge_filter = edge_filter
    #     self._max_depth = max_depth
    #     self._limit = limit
    #     self._function = function
    #     self._from = from_node
    #     self._to = to_node
    #     self._num_workers = num_workers