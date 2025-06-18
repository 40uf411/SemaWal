#!/usr/bin/python
# -*- coding=utf-8 -*-
from .node import Node

class Net(Node):
    """
    Represents a network of nodes.

    A Net is itself a Node, allowing networks to be nested. It manages a collection
    of nodes and provides methods for network-level operations like searching
    and pathfinding.

    Attributes:
        __desc (str): A description of the network.
        __index (dict): A dictionary mapping node names to Node objects for quick lookup.
        __nodes (list): A list of all Node objects directly within this network.
        __roots (list): A list of root nodes within this network.
        __nets (list): A list of sub-networks (Net objects) within this network.
    """
    def __init__(self, name="Network", description="", props={}, type="regular"):
        """
        Initializes a new Net.

        Args:
            name (str, optional): The name of the network. Defaults to "Network".
            description (str, optional): A description for the network. Defaults to "".
            props (dict, optional): Properties for the network node itself. Defaults to {}.
            type (str, optional): The type of the network node. Defaults to "regular".
        """
        super().__init__(name=name,props=props, type=type) 
        # self.__name is inherited from Node
        self.__desc = description
        self.__index = dict() # For quick node lookup by name
        self.__nodes = list() # All nodes in this net
        self.__roots = list() # Root nodes in this net
        self.__nets  = list() # Sub-networks in this net
        print(f"[SemaWal INFO] Created network: {name}")

    def desc(self):
        """
        Returns the description of the network.

        Returns:
            str: The network's description.
        """
        return self.__desc

    def set_description(self, description):
        """
        Sets the description for the network.

        Args:
            description (str): The new description.
        """
        self.__desc=description
        
    def append(self, node):
        """
        Adds a node to the network.

        If the node is already in the network, it's not added again.
        Keeps track of root nodes and sub-networks.

        Args:
            node (Node): The node to add.

        Returns:
            Net: The current Net instance, allowing for method chaining.
        """
        if node not in self.__nodes:
            self.__nodes.append(node)
            self.__index[node.name()] = node # Add to name-based index
            if isinstance(node, Node) and node.type() == "root":
                self.__roots.append(node)
            if isinstance(node, Net): # If the added node is also a Net
                self.__nets.append(node)
        return self

    def append_all(self, nodes):
        """
        Appends a list of nodes to the network.

        Args:
            nodes (list of Node): A list of Node objects to add.
        """
        for node in nodes:
            self.append(node)

    def drop(self, node):
        """
        Removes a node from the network.

        Also removes it from the index, list of roots, and list of sub-networks if applicable.

        Args:
            node (Node): The node to remove.

        Returns:
            Net: The current Net instance.
        """
        if node in self.__nodes:
            self.__nodes.remove(node)
            if node.name() in self.__index: # Check before deleting
                del self.__index[node.name()]
            if node in self.__roots:
                self.__roots.remove(node)
            if node in self.__nets:
                self.__nets.remove(node)
        return self

    def roots(self):
        """
        Returns a list of root nodes in this network.

        Returns:
            list: A list of Node objects that are roots.
        """
        return self.__roots

    def nodes(self):
        """
        Returns a list of all nodes in this network.

        Returns:
            list: A list of all Node objects.
        """
        return self.__nodes

    def get_node(self, nodeName):
        """
        Retrieves a node from the network by its name.

        Args:
            nodeName (str): The name of the node to retrieve.

        Returns:
            Node or None: The Node object if found, otherwise None (or raises KeyError if not checked).
        """
        return self.__index.get(nodeName) # Use .get() for safer access
    
    def nets(self):
        """
        Returns a list of sub-networks (Net objects) within this network.

        Returns:
            list: A list of Net objects.
        """
        return self.__nets
    
    def reset(self):
        """
        Resets the network, clearing all nodes, roots, index, and sub-networks.
        Also calls the parent Node's reset method.
        """
        super().reset() # Call parent Node's reset
        self.__nodes=list()
        self.__roots=list()
        self.__index=dict()
        self.__nets=list()
        print(f"[SemaWal INFO] Network '{self.name()}' has been reset.")

        
    def show_links(self, node=None):
        """
        Displays the links of nodes in the network.

        If a specific node is provided, it currently does nothing with it
        (commented out logic). If no node is provided, it iterates through all
        nodes in the network and calls their `show_links` method.

        Args:
            node (Node, optional): A specific node to show links for.
                Currently, this parameter is not fully utilized if provided.
                Defaults to None, which shows links for all nodes.
        """
        if node == None:
            for n_item in self.__nodes: # Renamed to avoid conflict with outer 'node'
                n_item.show_links()
        # elif isinstance(node, Node) and node in self.__nodes:
        #     # The commented out logic below seems to be an attempt at
        #     # displaying links of a node and its connections within the network.
        #     # It could be revived or redesigned if specific display logic is needed.
        #     toVisit = [node]
        #     visited = list()
        #     for n_visit in toVisit: # Renamed to avoid conflict
        #         n_visit.show_links()
        #         for nd_conn in n_visit.get_connections(): # Renamed
        #             if nd_conn not in visited and nd_conn in self.__nodes:
        #                 toVisit.append(nd_conn)
        #         visited.append(n_visit)
        #         if n_visit in toVisit : # Check before removing
        #            toVisit.remove(n_visit)


    def fetch(self, props = {}, type="all"):
        """
        Retrieves nodes from the network that match specified properties and type.

        Args:
            props (dict, optional): A property pattern to filter nodes.
                See `Node.validate_properties`. Defaults to {}.
            type (str, optional): The type of nodes to fetch ("regular", "root", "leaf").
                "all" fetches nodes of any type. Defaults to "all".

        Returns:
            list: A list of Node objects that match the criteria.
        """
        tmp = list()
        for node_item in self.__nodes: # Renamed to avoid conflict
            if (type == "all" or node_item.type() == type) and \
               node_item.validate_properties(props):
                tmp.append(node_item)
        return tmp

    def fetch_from(self, node, depth=-1, type="all", allowed_attributes=[], props={}, mode=-1, min_power=0, max_power=10, ignore_nodes=None, ignore_attributes=None): # Parameter names updated, ignore_attributes added
        """
        Recursively fetches nodes starting from a given node, based on connection criteria.

        Args:
            node (Node): The starting node for fetching.
            depth (int, optional): Maximum recursion depth. -1 for infinite. Defaults to -1.
            type (str, optional): Filter by node type ("all", "regular", "root", "leaf"). Defaults to "all".
            allowed_attributes (list, optional): List of link attributes to follow. Defaults to all. # Renamed
            props (dict, optional): Property filters for connections. Defaults to {}.
            mode (int, optional): Link mode filter (0 or 1). Defaults to -1 (any).
            min_power (int, optional): Minimum link power. Defaults to 0. # Renamed
            max_power (int, optional): Maximum link power. Defaults to 10. # Renamed
            ignore_nodes (list, optional): List of nodes to ignore during traversal. Automatically includes visited nodes. # Renamed & clarified
            ignore_attributes (list, optional): List of link attributes to ignore during traversal. Defaults to None. # Added

        Returns:
            list: A list of unique Node objects reachable from the start node matching the criteria.
        """
        # Ensure the starting node is part of the result.
        # Use a set for `collected_nodes` to handle uniqueness naturally.
        collected_nodes = {node} # Start with the initial node

        # Prepare a list of nodes to ignore in subsequent recursive calls.
        current_ignore_list = list(ignore_nodes) if ignore_nodes else [] # Initialize if None
        current_ignore_list.append(node) # Add the current node to the ignore list for deeper calls

        # Get direct connections from the current 'node' based on specified criteria
        # (attributes, properties of connected nodes, link mode, and power).
        connections = node.get_connections( # Calling Node's get_connections
            attributes=allowed_attributes, # Pass along
            props=props,
            mode=mode,
            min_power=min_power, # Pass along
            max_power=max_power, # Pass along
            ignore_attributes=ignore_attributes # Pass along
        )

        # Proceed with recursion only if the depth limit has not been reached.
        # depth == 0 means no more recursive steps are allowed.
        # depth == -1 means unlimited depth.
        if depth != 0:
            for connected_node in connections:
                # Consider a connected_node for further fetching if:
                # 1. It is part of the current network instance (`self.__nodes`).
                # 2. It has not been added to `current_ignore_list` in this path of recursion.
                if connected_node in self.__nodes and connected_node not in current_ignore_list:
                    # Recursively call fetch_from for the `connected_node`.
                    # The depth is decremented for the next level of recursion (if not unlimited).
                    # The `current_ignore_list` list is passed to ensure progress and avoid cycles.
                    # Results from the recursive call (a set of nodes) are added to `collected_nodes`.
                    collected_nodes.update(
                        self.fetch_from( # Changed here
                            connected_node,
                            depth=(depth-1) if depth > 0 else -1,
                            type=type,
                            allowed_attributes=allowed_attributes, # Renamed parameter
                            props=props,
                            mode=mode,
                            min_power=min_power, # Renamed parameter
                            max_power=max_power, # Renamed parameter
                            ignore_nodes=current_ignore_list, # Renamed parameter & passed updated list
                            ignore_attributes=ignore_attributes # Added parameter
                        )
                    )
        return list(collected_nodes) # Convert the set of unique nodes to a list before returning

    #, ignoredAttributes=[] # This was a comment in original code
    def find_path(self, nodeA, nodeB, depth=-1, allowed_attributes=[], props={}, mode=-1, min_power=0, max_power=10, ignore_nodes=None, ignore_attributes=None): # Parameter names updated, ignore_attributes added
        """
        Finds a path between two nodes (nodeA and nodeB) in the network.

        Uses a depth-first search approach, following links that match specified criteria.
        Only considers nodes present in the current network.

        Args:
            nodeA (Node): The starting node of the path.
            nodeB (Node): The target node of the path.
            depth (int, optional): Maximum path length (number of edges).
                -1 for unlimited. Defaults to -1.
            allowedAttributes (list, optional): Link attributes to follow. Defaults to [].
            props (dict, optional): Property pattern for intermediate nodes. Defaults to {}.
            mode (int, optional): Link mode to follow. Defaults to -1.
            minPower (int, optional): Minimum link power. Defaults to 0.
            maxPower (int, optional): Maximum link power. Defaults to 10.
            ignoreNodes (list, optional): Nodes to ignore during search.
                `nodeA` is added automatically. Defaults to [].

        Returns:
            list: A list of Node objects representing the path from nodeA to nodeB.
                  Returns an empty list if no path is found.
                  Example: [nodeA, intermediate_node, nodeB]
        """
        # Create a copy of the ignore_nodes list for this recursion level and add nodeA.
        # This prevents cycles and re-visiting nodes in the current path.
        current_ignore_list = list(ignore_nodes) if ignore_nodes else [] # Initialize if None
        current_ignore_list.append(nodeA)

        # Get direct connections from nodeA that match the specified link criteria.
        connections = nodeA.get_connections(
            attributes=allowed_attributes,
            props=props,
            mode=mode,
            min_power=min_power,
            max_power=max_power,
            ignore_attributes=ignore_attributes # Pass ignore_attributes
        )

        # Base condition 1: No further connections from nodeA based on criteria.
        # If there are no connections that meet the criteria, no path can be formed from nodeA.
        if not connections:
            return []

        # Base condition 2: Target nodeB is directly connected to nodeA. Path found.
        # This check implies nodeB itself must also satisfy 'props' if 'props' were provided to get_connections.
        if nodeB in connections:
            return [nodeA, nodeB]

        # Base condition 3: Depth limit reached.
        # If depth is 0, no more steps can be taken down this path.
        # (depth == -1 means unlimited depth, so this condition is not met).
        if depth == 0:
            return []

        # Recursive step: Explore paths through each connection.
        # The depth for the next recursive call is reduced by 1 if it's limited.
        # If depth is -1 (unlimited), it remains -1 for the next call.
        new_depth = depth - 1 if depth > 0 else -1

        for connected_node_candidate in connections:
            # Ensure the candidate node is part of the current network (`self.__nodes`)
            # and has not been visited in the current path exploration (`current_ignore_list`).
            if connected_node_candidate in self.__nodes and \
               connected_node_candidate not in current_ignore_list:

                # Recursively call find_path from the candidate node towards nodeB.
                path_segment = self.find_path(
                    nodeA=connected_node_candidate, # Start new search from this candidate
                    nodeB=nodeB,
                    depth=new_depth,
                    allowed_attributes=allowed_attributes, # Pass along
                    props=props,
                    mode=mode,
                    min_power=min_power, # Pass along
                    max_power=max_power, # Pass along
                    ignore_nodes=current_ignore_list, # Pass the updated ignore list
                    ignore_attributes=ignore_attributes # Pass along
                )

                # If the recursive call found a valid path segment (not empty)
                if path_segment:
                    # Prepend nodeA to the found segment to form the complete path from the original nodeA.
                    return [nodeA] + path_segment

        # If no path is found through any of the connections after checking all of them.
        return []

    def to_graphviz(self, generate_links=True):
        """
        Generates a DOT language representation of the network for Graphviz.

        Args:
            generate_links (bool, optional): Whether to ensure all static links are
                                           generated before creating the DOT output.
                                           Defaults to True.

        Returns:
            str: A string containing the DOT language representation of the network.
        """
        dot_lines = ["digraph SemaWalNetwork {"]
        dot_lines.append("  rankdir=LR; // Left to right layout")
        dot_lines.append("  node [shape=ellipse, style=filled, color=lightblue];")
        dot_lines.append("  edge [fontsize=10];")

        # Ensure all nodes commit their links if requested
        if generate_links:
            for node_obj in self.nodes(): # self.nodes() should return a list of Node objects
                node_obj.commit() # generate_static_links

        processed_nodes = set()

        for node_obj in self.nodes():
            node_name = node_obj.name()
            # Node already declared by a previous link traversal or parent check
            # if node_name in processed_nodes:
            #    continue # This might skip adding attributes if node was pre-declared by edge

            node_label = f"{node_name}\\n(Type: {node_obj.type()})" # Use \\n for newline in DOT
            # Add properties to label
            props_str_parts = []
            # Use get_properties() which should return a dict copy
            for key, value in node_obj.get_properties().items():
                props_str_parts.append(f"{key}: {value}")
            if props_str_parts:
                node_label += f"\\nProps: {', '.join(props_str_parts)}"

            node_attrs_list = [f'label="{node_label}"']
            if node_obj.type() == "root":
                node_attrs_list.append('shape=box')
                node_attrs_list.append('color=lightcoral')
            elif node_obj.type() == "leaf":
                node_attrs_list.append('shape=octagon')
                node_attrs_list.append('color=lightgreen')

            dot_lines.append(f'  "{node_name}" [{", ".join(node_attrs_list)}];')
            processed_nodes.add(node_name)

            # Add edges (links)
            # Ensure get_links is called on the node_obj
            node_links = node_obj.get_links(generate=False) # Links should be current due to earlier commit
            for attr, link_list in node_links.items():
                for target_node_info in link_list:
                    target_node, mode, power = target_node_info[0], target_node_info[1], target_node_info[2]
                    target_name = target_node.name()

                    # Ensure target node is also declared if it wasn't processed yet
                    # This is important if a linked node is not part of self.nodes() (e.g. external)
                    # or if it appears first as a target before its own loop.
                    if target_name not in processed_nodes:
                        # Check if it's a node within this network; if so, use its properties
                        # If it's an external node, just declare its name.
                        tn_label_str = f"{target_name}"
                        tn_attrs_list = []
                        if target_node in self.nodes(): # Is it a node managed by this network?
                             tn_label_str = f"{target_name}\\n(Type: {target_node.type()})"
                             tn_props_parts = []
                             for k,v in target_node.get_properties().items(): tn_props_parts.append(f"{k}: {v}")
                             if tn_props_parts: tn_label_str += f"\\nProps: {', '.join(tn_props_parts)}"
                             if target_node.type() == "root": tn_attrs_list.extend(['shape=box', 'color=lightcoral'])
                             elif target_node.type() == "leaf": tn_attrs_list.extend(['shape=octagon', 'color=lightgreen'])

                        tn_attrs_list.insert(0, f'label="{tn_label_str}"')
                        dot_lines.append(f'  "{target_name}" [{", ".join(tn_attrs_list)}];')
                        processed_nodes.add(target_name)


                    edge_attrs = [f'label="{attr} (P:{power})"']
                    if mode == 0: # Negative link
                        edge_attrs.append('color=red')
                        edge_attrs.append('style=dashed')
                    else: # Positive link
                        edge_attrs.append('color=darkgreen')

                    dot_lines.append(f'  "{node_name}" -> "{target_name}" [{", ".join(edge_attrs)}];')

        # Handle parent-child relationships from 'extends'
        for node_obj in self.nodes():
            parent_node = node_obj.parent()
            if parent_node is not None:
                # Ensure parent is declared (should be if it's part of the network,
                # or declared if it's an external parent)
                if parent_node.name() not in processed_nodes:
                    p_label_str = f"{parent_node.name()}"
                    p_attrs_list = []
                    if parent_node in self.nodes(): # Is parent managed by this network?
                        p_label_str = f"{parent_node.name()}\\n(Type: {parent_node.type()})"
                        # Add props to label for parent if desired
                        if parent_node.type() == "root": p_attrs_list.extend(['shape=box', 'color=lightcoral'])
                        # ... (other types for parent styling) ...
                    p_attrs_list.insert(0, f'label="{p_label_str}"')
                    dot_lines.append(f'  "{parent_node.name()}" [{", ".join(p_attrs_list)}];')
                    processed_nodes.add(parent_node.name())

                # Add 'extends' edge
                dot_lines.append(f'  "{node_obj.name()}" -> "{parent_node.name()}" [label="extends", style=dotted, arrowhead=onormal, color=blue];')


        dot_lines.append("}")
        return "\n".join(dot_lines)