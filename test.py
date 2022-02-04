from semawal import Node, Cluster

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