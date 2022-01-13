from msilib.schema import SelfReg
import uuid
# List of functions:
"""
- select all the paths between two Nodes while respecting the following criteria:
    - respecting the maximal depth.
    - respecting the given criteria on each Node (e.g. name, description, etc.).
    - respecting the given criteria on the edges between the Nodes.
    - the criteria on the edges can be a list of criteria, each of which will be evaluated on the edge with the corresponding depth.
- 
"""
class Term:
    def __init__(self):
        """ Initialize the term object.
        """
        self.__term_id = str(uuid.uuid4())
        self.__node_filters = []
        self.__edge_filters = []
