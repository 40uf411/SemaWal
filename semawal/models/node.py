import uuid
# Generate node model
class Node:
    # static variable of index type
    CONNECTION_TO_NODES = 0
    NODE_TO_CONNECTIONS = 1 
    # magic methods
    def __init__(self, name, description, attributes, parent = None) -> None:
        """Generate a node object.
        Args:
            name ([str]): Name of the node.
            description ([str]): Description of the node.
            attributes ([dict]): Attributes of the node.
            parent ([Node], optional): Parent node. Defaults to None.
        """
        self.__id = str(uuid.uuid4())
        self.__name = name if type(name) is str else ''
        self.__description = description if type(description) is str else ''
        self.__attributes = attributes if type(attributes) is dict else {}
        self.__parent = parent if type(parent) is Node else None
        self.__children = []
        self.__connections = {}
        self.__compiled_connection_nodes_index = {}
        self.__compiled_node_connections_index = {}
        self.__tmp = {
            "key": "",
            "power": 1,
            "allow": True,
            "props": {}
        }
    def __str__(self):
        """String representation of the node.
        Returns: [str]
        """
        return "%:%" % (self.__id, self.__name)
    def __repr__(self):
        """String representation of the node.
        Returns: [str]
        """
        return self.__str__()
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

    # Getters
    def get_id(self) -> str:
        """Get the node id.
        Returns:
            str: Node id.
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
    def get_attributes(self) -> dict:
        """Get the node attributes.
        Returns:
            dict: Node attributes.
        """
        return self.__attributes
    def get_attribute(self, key) -> any:
        """Get the node attribute.
        Args:
            key ([str]): Attribute key.
        Returns:
            dict: Node attribute.
        """
        return self.__attributes[key] if key in self.__attributes else None
    def get_parent(self) -> Node:
        """Get the node parent.
        Returns:
            Node: Node parent.
        """
        return self.__parent
    def get_children(self) -> list:
        """Get the node children.
        Returns:
            list: Node children.
        """
        return self.__children
    def get_connections(self, index=0) -> dict:
        """Get the node connections.
        Returns:
            dict: Node connections.
        """
        if index == 0:
            return self.__compiled_connection_nodes_index
        else:
            return self.__compiled_node_connections_index

    # Setters
    def set_name(self, name) -> None:
        """Set the node name.
        Args:
            name ([str]): Name of the node.
        """
        self.__name = name if type(name) is str else ''
    def set_description(self, description) -> None:
        """Set the node description.
        Args:
            description ([str]): Description of the node.
        """
        self.__description = description if type(description) is str else ''
    def set_attributes(self, attributes) -> None:
        """Set the node attributes.
        Args:
            attributes ([dict]): Attributes of the node.
        """
        self.__attributes = attributes if type(attributes) is dict else {}
    def set_attribute(self, key, value) -> None:
        """Set the node attribute.
        Args:
            key ([str]): Attribute key.
            value ([any]): Attribute value.
        """
        self.__attributes[key] = value
    def set_parent(self, parent) -> None:
        """Set the node parent.
        Args:
            parent ([Node]): Parent node.
        """
        self.__parent = parent if type(parent) is Node else None

    # Adders
    def add_child(self, child) -> None:
        """Add a child to the node.
        Args:
            child ([Node]): Child node.
        """
        self.__children.append(child)
    def add_connection(self, key, node, power = 1, allow = True, props = {}) -> None:
        """Add a connection to the node.
        Args:
            key ([str]): Connection key.
            node ([Node]): Connection node.
            power ([int], optional): Connection power. Defaults to 1.
            allow ([bool], optional): Connection allow. Defaults to True.
            props ([dict], optional): Connection properties. Defaults to {}.
        """
        if key in self.__connections:
            if node.get_id() not in self.__connections[key].keys():
                self.__connections[key][node.get_id()] = {
                    'power': power,
                    'allow': allow,
                    'props': props,
                    'node': node
                }
        else:
            self.__connections[key] = {
                node.get_id(): {
                    'power': power,
                    'allow': allow,
                    'props': props,
                    'node': node
                }
            }
        self.__tmp = {
            "power": power,
            "allow": allow,
            "props": props,
            'node': node
        }
    def and_with(self, node) -> None:
        """Add a connection to the node (this function uses the add_connection method).
        Args:
            node ([Node]): Connection node.
        """
        self.add_connection(self.__tmp['key'], node, self.__tmp['power'], self.__tmp['allow'], self.__tmp['props'])

    # Droppers
    def drop_child(self, child) -> None:
        """Drop a child from the node.
        Args:
            child ([Node]): Child node.
        """
        self.__children.remove(child)
    def drop_attribute(self, key) -> None:
        """Drop the node attribute.
        Args:
            key ([str]): Attribute key.
        """
        if key in self.__attributes:
            del self.__attributes[key]
    def drop_connection(self, key, node) -> None:
        """Drop the node connection.
        Args:
            key ([str]): Connection key.
        """
        if key in self.__connections and node.get_id() in self.__connections[key]:
            self.__connections[key].remove(node.get_id())
    def drop_parent(self) -> None:
        """Drop the node parent.
        """
        self.__parent = None

    # recetters
    def reset(self, full_reset = False) -> None:
        """Reset the node to default values.
        """
        if full_reset:
            self.__name = ""
            self.__description = ""
            self.__attributes = {}
        self.__parent = None
        self.__children = []
        self.__connections = {}
        self.__compiled_connection_nodes_index = {}
        self.__compiled_node_connections_index = {}
        self.__tmp = {
            "key": "",
            "power": 1,
            "allow": True,
            "props": {}
        }

    # Commit changes and generat static indexes
    def commit(self) -> None:
        """Commit the node changes.
        """
        tmp_connections = {}
        # check if the parent is not none, if so, get the parent connections
        if self.__parent is not None:
            tmp_connections = self.__parent.get_connections()
        # loop over the connections
        for connection_name, connections in self.__connections:
            for node_id, connection in connections.items():
                # check if the connection with the node is in the parent connections
                if connection_name not in tmp_connections.keys() or node_id not in tmp_connections[connection_name]:
                    if connection_name not in tmp_connections.keys():
                        tmp_connections[connection_name] = {
                            node_id: connection
                        }
                    else:
                        # if not, add the connection
                        tmp_connections[connection_name][node_id] = connection
                elif connection['power'] > tmp_connections[connection_name][node_id]['power']:
                    # if so, replace the parent connection with the current connection
                    tmp_connections[connection_name][node_id] = connection
        # set the compiled connections
        self.__compiled_connection_nodes_index = tmp_connections
        # compile the connections index
        self.__compiled_node_connections_index = {}
        for connection_name, connections in self.__compiled_connection_nodes_index.items():
            for node_id, connection in connections.items():
                if node_id in self.__compiled_node_connections_index:
                    self.__compiled_node_connections_index[node_id][connection_name] = connection
                else:                    
                    self.__compiled_node_connections_index[node_id] = {
                        connection_name: connection
                    }
        # notify the children
        for child in self.__children:
            child.commit()