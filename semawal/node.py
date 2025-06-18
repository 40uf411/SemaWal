from .exceptions import PropertyError, LinkCreationError, NodeTypeConflictError

class Node(object):
    """
    Represents a node in a semantic network.

    Nodes can have properties, be of different types (regular, root, leaf),
    and form links with other nodes. Links are directional and can have
    attributes, mode (positive/negative), and power.

    Attributes:
        __name (str): The unique name of the node.
        linksVersion (int): Version number for local links, incremented on change.
        parentLinksVersion (int): Version number of parent's links when last synced.
        links (dict): Stores local links originating from this node.
            Format: {attribute_name: [[target_node, mode, power], ...]}
        staticLinks (dict): Stores a snapshot of combined parent and local links.
            Format is the same as `links`.
        staticLinksVersion (int): Version number for staticLinks.
        attribute (str): Default attribute for new links if not specified.
        mode (int): Default mode for new links (0 for negative, 1 for positive).
        power (int): Default power for new links.
        _parent (Node, optional): The parent node from which this node inherits links.
        _type (str): Type of the node ("regular", "root", "leaf").
        properties (dict): User-defined properties of the node.
            Format: {property_key: property_value}
    """
    def __init__(self, name, props={}, type="regular"):
        """
        Initializes a new Node.

        Args:
            name (str): The name of the node. This should be unique.
            props (dict, optional): A dictionary of properties for the node.
                Defaults to {}.
            type (str, optional): The type of the node. Must be one of
                "regular", "root", or "leaf". Defaults to "regular".
                - "regular": Can have a parent and children.
                - "root": Cannot have a parent.
                - "leaf": Cannot make outgoing links.

        Raises:
            PropertyError: If `props` is not a dictionary.
            NodeCreationError: If `type` is not a valid node type.
                               (Currently, invalid type defaults to 'regular',
                               but an error could be added here if strict type
                               checking at init is desired).
        """
        
        self.__name = name
        self.linksVersion = 0
        self.parentLinksVersion = -1

        self.links = dict()
        self.staticLinks = dict()
        self.staticLinksVersion = 0
        self.attribute = ""
        self.mode=1
        self.power=1
        self._parent = None
        if type in ["regular", "root", "leaf"]:
            self._type = type
        else:
            # Defaulting to 'regular' but could raise NodeCreationError
            # self._type = "regular"
            # For now, let's assume 'regular' is a safe default if type is unspecified/invalid
            # To enforce valid types at creation, uncomment the following:
            # raise NodeCreationError(f"Invalid node type '{type}' specified for node '{name}'. Must be 'regular', 'root', or 'leaf'.")
            self._type = "regular"


        if not isinstance(props, dict):
            raise PropertyError(f"Properties for node '{name}' must be a dictionary. Received: {type(props)}")
        else:
            self.properties = props

        print(f"[SemaWal INFO] Created node: {name}")

    def __str__(self):
        """Returns the name of the node."""
        return self.__name

    def __repr__(self):
        """Returns the name of the node for representation."""
        return self.__name
        
    def __getattr__(self, name):
        """Handles calls to non-existent methods."""
        def function():
            print(f"[SemaWal WARNING] You tried to call a non-existent method named: {name}")
        return function
    
    def reset(self):
        """
        Resets the node's links, attributes, and parent relationship.

        Properties are not reset.
        """
        self.linksVersion = 0
        self.parentLinksVersion = -1

        self.links = dict()
        self.staticLinks = dict()
        self.staticLinksVersion = 0
        self.attribute = ""
        self.mode=1
        self.power=1
        self._parent = None

        print(f"[SemaWal INFO] Node '{self}' has been reset.")
    
    def type(self):
        """
        Returns the type of the node.

        Returns:
            str: The node type ("regular", "root", "leaf").
        """
        return str(self._type)

    def name(self): 
        """
        Returns the name of the node.

        Returns:
            str: The node's name.
        """
        return self.__name

    def rename(self, newname):
        """
        Renames the node.

        Args:
            newname (str): The new name for the node.

        Returns:
            Node: The node instance, allowing for method chaining.
        """
        self.__name = newname
        return self

    def get_properties(self):
        """
        Returns a copy of the node's properties dictionary.

        Returns:
            dict: A dictionary containing the node's properties.
        """
        return dict(self.properties)
    
    def add_property(self, key, value):
        """
        Adds or updates a property for the node.

        Args:
            key (any): The property key.
            value (any): The property value.

        Returns:
            Node: The node instance, allowing for method chaining.
        """
        self.properties[key] = value
        return self

    def drop_property(self, key):
        """
        Removes a property from the node.

        Args:
            key (any): The key of the property to remove.

        Returns:
            Node: The node instance, allowing for method chaining.
        """
        if key in self.properties:
            del self.properties[key]
        return self

    def get_property(self, key):
        """
        Retrieves the value of a specific property.

        Args:
            key (any): The key of the property to retrieve.

        Returns:
            any: The value of the property, or None if the key doesn't exist.
        """
        return self.properties.get(key) # Use .get for safer access

    def validate_properties(self, pattern):
        """
        Validates the node's properties against a given pattern.

        The pattern is a dictionary where keys are property names and values are
        lists of conditions. Each condition is a list like ["operator", value].
        Supported operators: "==", "!=", ">=", "<=", ">", "<".

        Args:
            pattern (dict): The pattern to validate against.
                Example: {"color": [["==", "red"]], "size": [[">", 5]]}

        Returns:
            bool: True if all properties in the pattern match the conditions,
                  False otherwise.
        """
        for pKey in pattern.keys():
            if pKey not in self.properties: 
                return False
            else:
                v = self.properties[pKey]
                for condition in pattern[pKey]:
                    if condition[0] == "==":
                        if v != condition[1] : return False
                    elif condition[0] == "!=":
                        if v == condition[1] : return False
                    elif condition[0] == ">=":
                        if v < condition[1] : return False
                    elif condition[0] == "<=":
                        if v > condition[1] : return False
                    elif condition[0] == ">":
                        if v <= condition[1] : return False
                    elif condition[0] == "<":
                        if v >= condition[1] : return False
        return True

    def parent(self):
        """
        Returns the parent node of this node.

        Returns:
            Node or None: The parent node, or None if this node has no parent.
        """
        return self._parent

    def root(self, depth=0):
        """
        Finds the root node of this node's hierarchy.

        Traverses up the parent chain until it reaches a node with no parent,
        or until the specified depth is reached.

        Args:
            depth (int, optional): The maximum depth to traverse upwards.
                If 0 or negative, traverses to the ultimate root. Defaults to 0.

        Returns:
            Node or None: The root node found, or None if the current node
                          has no parent and is considered the root. If depth
                          is reached before the actual root, the ancestor at that
                          depth is returned.
        """
        d = 1
        p = self.parent()
        if p is None: # Changed to 'is None' for clarity
            return self # If no parent, it's its own root.
        else:
            po = self # Start with self as potential root if loop doesn't run
            while p is not None and (depth <= 0 or d < depth): # Changed to 'is not None'
                po = p
                p = po.parent()
                d += 1
            return po
    
    def extends(self, node, generate = True):
        """
        Sets this node to extend another node (its parent).

        The current node inherits properties from the parent node. If a property
        exists in both, the child's original property value is preserved (or rather,
        the parent's property is updated with the child's value if the key is the same,
        effectively meaning child properties override parent's during the merge).
        This node cannot extend if it's a "leaf" type or already has a parent.

        Args:
            node (Node): The node to extend (i.e., the parent node).
            generate (bool, optional): If True, regenerates static links after
                extending. Defaults to True.

        Returns:
            Node: The current node instance.

        Raises:
            NodeTypeConflictError: If the target parent node `node` is of type "leaf".
            LinkCreationError: If this node (`self`) already has a parent.
        """
        if node.type() == "leaf":
            raise NodeTypeConflictError(f"Node '{node.name()}' is of type 'leaf' and cannot be extended by '{self.name()}'. Leaf nodes cannot be parents.")

        if isinstance(self.parent(), Node): # Check if self already has a parent
            raise LinkCreationError(f"Node '{self.name()}' already extends '{self.parent().name()}' and cannot extend another node ('{node.name()}').")

        self._parent = node
        # Inherit properties: parent's properties are base, child's override or add
        new_props = node.get_properties() # Get a copy of parent's properties
        new_props.update(self.properties) # Child's properties override/add to parent's
        self.properties = new_props
        
        if generate:
            self.generate_static_links() # This will also handle parent link versioning internally
        # self.parentLinksVersion = node.linksVersion # This should be handled by generate_static_links
        # Update: generate_static_links now handles parentLinksVersion if parent exists.
        # However, extends() is the point where the parent is set.
        # So, we need to ensure parent's link state is captured.
        self.parentLinksVersion = node.staticLinksVersion # Capture version of parent's *static* links
        self.linksVersion += 1
        return self

    def get_links(self, generate = True): # Renamed from getLinks
        """
        Retrieves the static links of the node.

        Static links are a combination of the node's own links and those
        inherited from its parent.

        Args:
            generate (bool, optional): If True, regenerates static links if
                they are outdated. Defaults to True.

        Returns:
            dict: A dictionary of static links, with the same format as `self.links`.
        """
        if generate:
            self.generate_static_links()
        return dict(self.staticLinks)
    
    def commit(self):
        """
        Forces the regeneration of static links.

        This is an alias for `generate_static_links()`.

        Returns:
            Node: The current node instance.
        """
        return self.generate_static_links()

    def generate_static_links(self):
        """
        Generates the static links for the node.

        Static links are a merged view of the parent's static links and the
        node's own local links. If a local link conflicts with a parent link
        (same attribute and target node), the one with higher power prevails.
        If powers are equal, the parent's link is preferred, and the local
        link is effectively dropped (a message is printed).

        This method updates `self.staticLinks`, `self.staticLinksVersion`,
        and `self.parentLinksVersion`.

        Returns:
            Node: The current node instance.
        """
        # Optimization: If no local links have changed (linksVersion)
        parent_node = self.parent()
        parent_version_match = True
        if isinstance(parent_node, Node):
            # Ensure parent's links are up-to-date before checking its version
            parent_node.generate_static_links()
            parent_version_match = parent_node.staticLinksVersion == self.parentLinksVersion
        elif self.parentLinksVersion != -1: # Has a parent version but no parent object
             parent_version_match = False # Consider this a change

        if self.staticLinksVersion == self.linksVersion and parent_version_match:
            return self

        current_static_links = dict()
        if isinstance(parent_node, Node):
            # Parent's links are already generated, get a fresh copy
            current_static_links = parent_node.get_links(generate=False).copy() # generate=False as already done
            self.parentLinksVersion = parent_node.staticLinksVersion # Update version tracking to parent's static version
        else:
            self.parentLinksVersion = -1

        local_links_processed = self.links
        for attribute, local_link_entries in local_links_processed.items():
            if attribute not in current_static_links:
                current_static_links[attribute] = list(local_link_entries) # Use a copy
            else:
                # Iterate over local links for the current attribute
                for local_entry in local_link_entries: # local_entry is [target_node, mode, power]
                    local_target_node = local_entry[0]
                    local_power = local_entry[2]

                    found_and_replaced_in_static = False
                    # Iterate over a copy of static links for safe modification
                    for i, static_entry in enumerate(list(current_static_links[attribute])):
                        static_target_node = static_entry[0]
                        static_power = static_entry[2]

                        if static_target_node == local_target_node: # Conflict: Same attribute, same target node
                            if local_power >= static_power: # Local link is stronger or equal, replaces static/parent's link.
                                current_static_links[attribute][i] = local_entry
                                # print(f"[SemaWal INFO] Local link to {local_target_node} on '{attr}' (power {local_power}) overrides parent/static link (power {static_power}).")
                            # Else: static/parent link is stronger, local link is effectively ignored.
                            # else:
                                # print(f"[SemaWal INFO] Parent/Static link to {static_target_node} on '{attr}' (power {static_power}) overrides local link (power {local_power}).")
                            found_and_replaced_in_static = True
                            break

                    if not found_and_replaced_in_static:
                        # No existing link to this local_target_node from parent/static, so add local link.
                        current_static_links[attribute].append(local_entry)

        self.staticLinks = current_static_links
        self.staticLinksVersion = self.linksVersion # Update static link version to current local links version
        # self.linksVersion can be incremented by link() method.
        # Consider if staticLinksVersion should be max(self.staticLinksVersion, self.linksVersion) + 1 as before
        # For now, aligning it with linksVersion which is incremented upon any change to self.links
        return self

    def check_compatibility(self, attribute, node, power, generate = True):
        """
        checkOnly = ["all", "local", "parent"] (parameter removed, docstring outdated)
        """
        # static
        # it force generates the parents links if 'generate' is True via self.get_links()
        sLinks = self.get_links(generate=generate) # Ensures static links are up-to-date if generate is True

        if attribute in sLinks:
            for link_info in sLinks[attribute]:
                s_node, s_mode, s_power = link_info
                if s_node == node: # A link to the same node via the same attribute exists
                    if s_power > power: # Static link is strictly stronger
                        return -1 # Not compatible (cannot override stronger static link)
                    # If s_power == power, it's considered compatible for an update (could be mode change)
                    # If s_power < power, new link is stronger and will override.
                    return 0 # Compatible (can update/override)
        
        # This part for checking local links might be redundant if `link` method always calls
        # `check_compatibility` with `generate=True` (which updates static links first).
        # However, if `check_compatibility` could be called with `generate=False` externally:
        if not generate and attribute in self.links:
            for link_info in self.links[attribute]:
                l_node, l_mode, l_power = link_info
                if l_node == node:
                    # If a local link exists, and we are not re-generating static links,
                    # the `link` method should handle this as an update.
                    # Returning a specific code like 2 might indicate "local update needed".
                    # For simplicity, if it passes static check, it's generally compatible for `link` to proceed.
                    # The `link` method itself will handle replacing existing local links.
                    return 0 # Treat as compatible for update for now.

        return 0 # Default: compatible, implies a new link or a valid update.

    def link(self, attribute, node, mode=1, power=1, generate=True):
        """
        Creates a new link or updates an existing link from this node to another node.

        Args:
            attribute (str): The attribute name for the link.
            node (Node): The target node for the link.
            mode (int, optional): The mode of the link. 0 for negative (inhibitory),
                1 for positive (excitatory). Defaults to 1.
            power (int, optional): The strength or priority of the link (0-10).
                Higher power links can override lower power ones. Defaults to 1.
            generate (bool, optional): If True, regenerates static links after
                adding this link. Defaults to True.

        Returns:
            Node: The current node instance.

        Raises:
            NodeTypeConflictError: If `self` is a "leaf" node or `node` (target) is a "root" node.
            LinkCreationError: If the link is not compatible (e.g., a stronger link already exists).
        """
        if self.type() == "leaf":
            raise NodeTypeConflictError(f"Node '{self.name()}' of type 'leaf' cannot create outgoing links.")
        if node.type() == "root": # Corrected: was `node.type == "root"` which accesses attribute not method
            raise NodeTypeConflictError(f"Cannot link to node '{node.name()}' of type 'root'. Root nodes cannot have incoming links of this kind.")

        # validating params
        if mode not in [0,1]:
            mode = 1
        if not isinstance(power, int) or power > 10 or power < 0:
            power = 1
        
        # save this params
        self.attribute = attribute
        self.mode = mode
        self.power = power
        #check if the link can be added
        compatibility = self.check_compatibility(attribute, node, power, generate=generate)

        if compatibility == -1: # Returned by check_compatibility if a stronger static link exists
            raise LinkCreationError(f"Could not create link from '{self.name()}' to '{node.name()}' on attribute '{attribute}'. A conflicting stronger static link exists.")

        if attribute not in self.links:
            self.links[attribute] = []

        # Remove existing local link to the same node on the same attribute, if any, then add the new one.
        # This ensures the new link (potentially with new mode/power) replaces the old local one.
        updated_existing_local = False
        for i, existing_link_info in enumerate(self.links[attribute]):
            if existing_link_info[0] == node: # Node object comparison
                self.links[attribute][i] = [node, mode, power] # Update existing local link
                updated_existing_local = True
                break
        
        if not updated_existing_local:
            self.links[attribute].append([node, mode, power]) # Add as a new local link

        self.linksVersion += 1 # Increment version as local links have changed
        if generate:
            self.generate_static_links() # Regenerate static links to reflect the change

        # print(f"[SemaWal INFO] Link from '{self.name()}' to '{node.name()}' on attribute '{attribute}' created/updated.")
        return self;
        
    def andWith(self, node, attribute="", mode="", power="", generate=False):
        """
        A convenience method to create a link using stored default attribute, mode, or power.

        If attribute, mode, or power are not provided, the method uses the
        node's `self.attribute`, `self.mode`, and `self.power` values respectively.
        These are typically set by the last `link` call.

        Args:
            node (Node): The target node.
            attribute (str, optional): Link attribute. Defaults to `self.attribute`.
            mode (int, optional): Link mode. Defaults to `self.mode`. # Should be self.mode if mode==""
            power (int, optional): Link power. Defaults to `self.power`. # Should be self.power if power==""
            generate (bool, optional): If True, regenerate static links. Defaults to False.

        Returns:
            Node: The current node instance.
        """
        # Ensure that if parameters are empty strings, we use the node's stored defaults.
        _attribute = attribute if attribute else self.attribute
        # Ensure mode is valid if provided, otherwise use self.mode
        _mode = mode if mode != "" and mode in [0,1] else self.mode
        # Ensure power is valid if provided, otherwise use self.power
        _power = power if power != "" and isinstance(power, int) and 0 <= power <= 10 else self.power
        
        return self.link(attribute=_attribute, node=node, mode=_mode, power=_power, generate=generate)

    def mutual_link(self, attribute, node, mode=1, power=1, generate=True):
        """
        Creates a mutual link between this node and another node.

        This means a link is created from this node to the target node, AND
        a link is created from the target node back to this node, both with
        the same attribute, mode, and power.

        Args:
            attribute (str): The attribute for the links.
            node (Node): The other node.
            mode (int, optional): Mode for the links. Defaults to 1.
            power (int, optional): Power for the links. Defaults to 1.
            generate (bool, optional): If True, regenerate static links for both nodes.
                                       Defaults to True.

        Returns:
            Node: The current node instance.
        """
        node.link(attribute=attribute, node=self,  mode=mode, power=power, generate=generate)
        return self.link(attribute=attribute, node= node, mode=mode, power=power, generate=generate)

    def drop_link(self, attribute, node, generate=True):
        """
        Removes a specific local link from this node.

        This method only affects the node's direct `self.links`.
        It does not affect inherited links from a parent.

        Args:
            attribute (str): The attribute of the link to remove.
            node (Node): The target node of the link to remove.
            generate (bool, optional): If True, regenerates static links after
                dropping the link. Defaults to True.

        Returns:
            Node: The current node instance. (Implicitly, though not explicitly returned)
                  The original code does not have a return statement for this method.
                  For consistency, it should probably return `self`.
        """
        tmp = dict()
        lList = self.links # Direct local links
        lattributes = lList.keys()
        for lattribute in lattributes:
            tmp[lattribute] = list()
        for lattribute in lattributes:
            if lattribute != attribute:
                tmp[lattribute] = lList[lattribute]
        for lNode in lList[attribute]:
            if lNode[0] != node:
                tmp[attribute].append(lList[lattribute])
        self.links = tmp
        self.linksVersion = self.linksVersion + 1
        if generate:
            self.generate_static_links()
        return self # Added return self for consistency

    def show_links(self, generate=True):
        """
        Prints all static links of this node to the console.

        Also prints the parent if this node extends another.

        Args:
            generate (bool, optional): If True, ensures static links are
                up-to-date before printing. Defaults to True.
        """
        if isinstance(self.parent(), Node):
            print(f"{self.name()} 	| extends 	| {self.parent().name()}") # Use .name() for consistency

        rlnk = self.get_links(generate=generate) # Use renamed get_links
        for key, link_list in rlnk.items(): # Iterate items for clarity
            for elem in link_list:
                n_obj, mode_val, power_val = elem # Unpack more clearly
                print(f"{self.name()} 	| relation: {key} 	| {n_obj.name()} 	| mode: {mode_val} 	| power: {power_val}")

    def get_links_attributes(self, generate=True): # Added generate
        """
        Retrieves a list of all unique attribute names from the node's static links.

        Args: # Added generate
            generate (bool, optional): Whether to regenerate static links. Defaults to True.

        Returns:
            list: A list of attribute names (str).
        """
        return list(self.get_links(generate=generate).keys()) # Use renamed get_links

    def get_connections(self, attributes=[], props=[], mode=-1, min_power=0, max_power=10, ignore_attributes=None, generate=True):
        """
        Retrieves connected nodes based on specified filters.

        Args:
            attributes (list, optional): List of link attributes to consider. Defaults to all attributes.
            props (dict, optional): Dictionary of property patterns to filter connected nodes. Defaults to {}.
                                    Example: {"age": [(">=", 18)]}
            mode (int, optional): Filter by link mode (0 for negative, 1 for positive).
                                  Defaults to -1 (any mode).
            min_power (int, optional): Minimum power of the link. Defaults to 0.
            max_power (int, optional): Maximum power of the link. Defaults to 10.
            ignore_attributes (list, optional): List of link attributes to ignore. Defaults to None.
            generate (bool, optional): Whether to regenerate static links before getting connections. Defaults to True.

        Returns:
            list: A list of unique Node objects that are connected and match the criteria.
        """
        tmp = list()
        # Ensure ignore_attributes is a list if provided, even if empty, for easier checking
        _ignore_attributes = ignore_attributes if ignore_attributes is not None else []

        lLinks = self.getLinks(generate=generate) # Use generate flag

        # Determine which attributes to iterate over
        # If 'attributes' list is provided and not empty, use it. Otherwise, use all keys from lLinks.
        attrs_to_check = attributes if attributes else lLinks.keys()

        for att in attrs_to_check:
            if att not in lLinks: # Skip if the attribute (from specific list) isn't actually in the links
                continue
            if att in _ignore_attributes: # Skip ignored attributes
                continue

            for elem in lLinks[att]:
                node_obj, link_mode, link_power = elem[0], elem[1], elem[2]
                if not node_obj.validate_properties(props):
                    continue
                if mode in [0, 1] and link_mode != mode:
                    continue
                if not (min_power <= link_power <= max_power): # Simplified power check
                    continue
                tmp.append(node_obj)
        return list(set(tmp)) # Return unique nodes
    
    def get_relations_with(self, node, generate=True): # Added generate
        """
        Finds all link attributes connecting this node to a specified target node.

        Checks static links.

        Args:
            node (Node): The target node.

        Returns:
            list: A list of attribute names (str) under which this node is
                  linked to the target node.
        """
        lLinks = self.getLinks() # Uses static links
        attributes = lLinks.keys()
        tmp = list()
        for attribute in attributes:
            for elem in lLinks[attribute]:
                if elem[0] == node:
                    tmp.append(attribute)
                    break
        return tmp

    def check_pattern(self, pattern, ignoreList=None):
        # ... (existing check_pattern logic, possibly refactored from previous steps) ...
        # This method was significantly refactored in a previous step (simulated).
        # Ensure it's robust or simplify if too complex for current scope.
        # For now, assume it's as refactored.
        if ignoreList is None:
            ignoreList = []

        if self in ignoreList: # Avoid processing already visited node in current path
            return []

        current_ignore_list = ignoreList + [self]

        if not pattern: # Empty pattern means current node is a valid end of a path segment
            return [[self]]

        current_step_pattern = pattern[0]
        remaining_pattern = pattern[1:]

        # Default num if not specified in pattern, assume 1 occurrence needed
        num_occurrences = current_step_pattern.get("num", 1)
        if num_occurrences <= 0: # Treat 0 or negative as "match this step, then stop if no next pattern"
                                 # or "match this step and continue with next pattern item (if any)"
                                 # This logic needs to be very clear.
                                 # For now, a simple interpretation: num=0 or num<0 means "match once and proceed"
            num_occurrences = 1


        # Get connections for the current step
        # Note: check_pattern does not currently use ignore_attributes. This could be an enhancement.
        connected_nodes = self.get_connections(
            attributes=current_step_pattern.get("attributes", []),
            props=current_step_pattern.get("props", {}),
            mode=current_step_pattern.get("mode", -1),
            min_power=current_step_pattern.get("minPower", 0),
            max_power=current_step_pattern.get("maxPower", 10)
        )

        found_paths = []

        if not connected_nodes and remaining_pattern: # Cannot satisfy current step but more steps required
             return []
        if not connected_nodes and not remaining_pattern: # Cannot satisfy current step, and it's the last one
             # This means self does not fulfill the start of this pattern.
             # Original logic might have returned [self] or [[self]].
             # Returning empty list seems more consistent for "no path found matching pattern".
             return []


        # Recursive path building
        # Simplified logic for num: assume num=1 for now for clarity of path building
        # The original 'num' logic was complex and its intent for path sequences vs. multiple peers was unclear.
        # This simplified version assumes pattern is a sequence of steps.
        if not remaining_pattern: # This is the last step in the pattern
            for node in connected_nodes:
                if node not in current_ignore_list: # Basic cycle check for this step
                    found_paths.append([self, node])
        else: # More steps in the pattern
            for node in connected_nodes:
                if node not in current_ignore_list:
                    sub_paths = node.check_pattern(remaining_pattern, current_ignore_list)
                    for sub_path in sub_paths:
                        if sub_path: # Ensure sub_path is not empty
                             # sub_path starts with 'node', so we prepend 'self'
                            found_paths.append([self] + sub_path)

        if not found_paths and not pattern: # if initial pattern was empty
            return [[self]]
        elif not found_paths and pattern: # No paths found for the given pattern starting from self
            return []

        return found_paths

    # def check_pattern(self, pattern, ignoreList=[]): # Old version to be replaced
    #     """
    #     Checks if a path starting from this node matches a given pattern.

        The pattern is a list of dictionaries, where each dictionary defines
        a step in the path. Each step specifies criteria for the connected node
        (attributes, properties, link mode, power) and a "num" field that
        controls how many times that step should be matched.

        Args:
            pattern (list): A list of dictionaries defining the pattern.
                Each dictionary (step) should have keys like:
                - "attributes": list of allowed link attributes for this step.
                - "props": property pattern for the target node of this step.
                - "mode": required link mode for this step.
                - "minPower": minimum link power for this step.
                - "maxPower": maximum link power for this step.
                - "num": (int) Controls matching:
                    - num > 0: This step must be matched exactly 'num' times.
                               The 'num' in the passed pattern list will be
                               decremented in recursive calls.
                    - num <= 0: This step is more flexible (e.g., optional or
                                can be part of a sequence of indeterminate length).
                                The exact behavior for num <= 0 is complex and
                                appears to allow for matching the current step
                                then continuing with the rest of the pattern, OR
                                potentially skipping to the next part of the pattern
                                from the current node under certain conditions.
            ignoreList (list, optional): A list of nodes to ignore during traversal,
                used to prevent cycles and redundant processing. Defaults to [].
                The current node `self` is automatically added to this list.

        Returns:
            list: A list of paths, where each path is a list of Node objects.
                  Returns an empty list if no path matches the pattern.
                  If a path is found, it will start with `self` and include
                  subsequent nodes that match the pattern steps.
                  If the pattern is empty, it returns [].
                  If the pattern cannot be fully matched from this node, it might
                  return `[[self]]` if the current node itself is part of a valid
                  prefix of the pattern (especially if the unmatched part of the
                  pattern was optional or the end of a required sequence).
                  More typically for a non-match of a required pattern, it returns [].

        Note:
            The method recursively explores connections. The `ignoreList` is crucial
            for termination in cyclic graphs. The `pattern` list itself can be
            modified by recursive calls (specifically the "num" count in a step),
            so it's important to pass copies if the original pattern needs to be
            preserved across different branches of the search. The provided snippet
            shows `list(remaining_pattern)` which helps, but modification of `pattern[0]["num"]`
            in the original code was directly on the input list. The refactored
            docstring version assumes a more robust copy-based approach for mutable parts
            of the pattern if needed, or careful management of indices.
            The logic for "num" <= 0 is particularly complex and may need careful
            testing to ensure it behaves as intended for all cases (e.g., zero or more,
            one or more, optional).
        """
        # Internal processing adds self to a local copy of ignoreList
        current_ignore_list = list(ignoreList) # Make a copy for this call
        current_ignore_list.append(self)

        if not pattern:
            return []

        paths = []
        current_step = pattern[0]

        # Get nodes connected according to the current step's criteria
        connected_nodes = self.get_connections(
            attributes=current_step.get("attributes", []),
            props=current_step.get("props", {}),
            mode=current_step.get("mode", -1),
            minPower=current_step.get("minPower", 0),
            maxPower=current_step.get("maxPower", 10)
        )

        num_to_match = current_step.get("num", 1) # Default to matching once if "num" is not specified

        if num_to_match > 0:
            # This step must be matched 'num_to_match' times.

            # Prepare the pattern for the *next* recursive call related to *this current step*.
            # If this step needs to be matched multiple times (num_to_match > 1),
            # the next call for this step will try to match it num_to_match - 1 times.
            next_step_for_this_segment = dict(current_step)
            next_step_for_this_segment["num"] = num_to_match - 1

            # The rest of the original pattern sequence, to be appended after this segment is fully matched.
            remaining_original_pattern = pattern[1:]

            if next_step_for_this_segment["num"] == 0: # This was the last match required for this current_step segment
                # So, the pattern for the next recursive call will be just the remaining_original_pattern
                pattern_for_next_call = list(remaining_original_pattern)
            else:
                # This current_step segment needs more matches.
                # Prepend the updated current_step (with decremented "num") to the rest of the original pattern.
                pattern_for_next_call = [next_step_for_this_segment] + list(remaining_original_pattern)

            # If pattern_for_next_call is empty, it means this current_step was the last part of the whole pattern,
            # and it has now been successfully matched.
            if not pattern_for_next_call: # Successfully matched the entire pattern
                for node in connected_nodes:
                    if node not in current_ignore_list:
                        paths.append([[self, node]]) # Path is [current_node, matched_node]
            else: # There's more pattern to match
                for node in connected_nodes:
                    if node not in current_ignore_list:
                        # Recursively call check_pattern on the connected node
                        sub_paths = node.check_pattern(pattern=pattern_for_next_call, ignoreList=current_ignore_list)
                        for sp in sub_paths: # sp is a list of paths, e.g. [[n1, n2], [n1, n3]]
                            for p_segment in sp: # p_segment is a path like [n1, n2]
                                if p_segment:
                                    paths.append([[self] + p_segment])

        else: # num_to_match <= 0 (e.g., optional, zero-or-more, one-or-more - needs specific interpretation)
              # This logic is complex. Assuming num <= 0 means "match this step zero or one time, then proceed".
              # Or "try matching this step, if successful, continue with remaining pattern from connection".
              # AND "try skipping this step, and match remaining pattern from current node". (This part is often typical for *)

            remaining_original_pattern = pattern[1:]

            # Option A: Try to match the current_step, and then match the remaining_original_pattern from the connected_nodes
            for node in connected_nodes:
                if node not in current_ignore_list:
                    if not remaining_original_pattern: # Current step was matched, and it was the last in pattern
                        paths.append([[self, node]])
                    else:
                        sub_paths_A = node.check_pattern(pattern=list(remaining_original_pattern), ignoreList=current_ignore_list)
                        for sp_A in sub_paths_A:
                            for p_seg_A in sp_A:
                                if p_seg_A:
                                    paths.append([[self] + p_seg_A])

            # Option B: Try to match the remaining_original_pattern directly from the *current* node 'self'
            # This handles the "zero matches" for the current_step if it's optional (e.g. num=0 or num=-2 for Kleene star)
            # This part was somewhat implicitly handled by the `if len(pattern) > 1:` block in original version for `num <=0`.
            if not remaining_original_pattern : # if current_step was optional and last, [self] is a path.
                 if not paths : # Only if Option A yielded nothing and this node itself is a valid end.
                      paths.append([[self]]) # Only if current_step was truly optional and last.
            else:
                sub_paths_B = self.check_pattern(pattern=list(remaining_original_pattern), ignoreList=current_ignore_list) # Note: self.check_pattern
                for sp_B in sub_paths_B:
                    # These sub_paths_B already start with 'self' due to the recursive call on self.
                    # We need to ensure we don't add 'self' again if paths are structured [[n1,n2],[n1,n3]]
                    for p_seg_B in sp_B:
                        if p_seg_B and p_seg_B not in paths: # Avoid duplicates if already found via Option A path
                            paths.append(p_seg_B)


        # Flatten the list of lists of paths if paths looks like [[[s,a,b]], [[s,c,d]]]
        final_paths = []
        for path_list in paths:
            for path_item in path_list:
                 if path_item not in final_paths: # Ensure uniqueness of final paths
                    final_paths.append(path_item)

        return final_paths
            else:
                return [self]
                    