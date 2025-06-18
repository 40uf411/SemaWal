import unittest
from semawal.node import Node
from semawal.net import Net

class TestNet(unittest.TestCase):

    def setUp(self):
        self.net = Net("TestNetwork")
        self.n1 = Node("n1_in_net", props={"id": 1})
        self.n2 = Node("n2_in_net", props={"id": 2, "status": "active"})
        self.n3 = Node("n3_in_net", props={"id": 3, "status": "inactive"})
        self.n4 = Node("n4_in_net", props={"id": 4, "status": "active"})

        self.net.append_all([self.n1, self.n2, self.n3, self.n4])

        # n1 -> n2 (rel_a)
        # n1 -> n3 (rel_b)
        # n2 -> n4 (rel_a)
        self.n1.link("rel_a", self.n2)
        self.n1.link("rel_b", self.n3)
        self.n2.link("rel_a", self.n4)
        self.n1.commit()
        self.n2.commit()


    def test_network_creation_and_nodes(self):
        self.assertEqual(self.net.name(), "TestNetwork")
        self.assertEqual(len(self.net.nodes()), 4)
        self.assertIn(self.n1, self.net.nodes())

        node_by_name = self.net.get_node("n1_in_net")
        self.assertEqual(node_by_name, self.n1)
        self.assertIsNone(self.net.get_node("non_existent_node"))

        self.net.drop(self.n4)
        self.assertEqual(len(self.net.nodes()), 3)
        self.assertNotIn(self.n4, self.net.nodes())
        self.assertIsNone(self.net.get_node("n4_in_net"))
        # Re-add for other tests
        self.net.append(self.n4)


    def test_fetch_nodes(self):
        active_nodes = self.net.fetch(props={"status": [("==", "active")]})
        self.assertEqual(len(active_nodes), 2)
        self.assertIn(self.n2, active_nodes)
        self.assertIn(self.n4, active_nodes)

        id_3_node = self.net.fetch(props={"id": [("==", 3)]})
        self.assertEqual(len(id_3_node), 1)
        self.assertIn(self.n3, id_3_node)

        # Test fetch by type (assuming all are 'regular' by default)
        regular_nodes = self.net.fetch(type="regular")
        self.assertEqual(len(regular_nodes), len(self.net.nodes()))

        leaf_nodes_in_net = Net("LeafNet")
        leaf_node = Node("leafy_in_net", type="leaf")
        leaf_nodes_in_net.append(leaf_node)
        fetched_leaf = leaf_nodes_in_net.fetch(type="leaf")
        self.assertEqual(len(fetched_leaf), 1)
        self.assertIn(leaf_node, fetched_leaf)


    def test_find_path(self):
        # Path: n1 -> n2 -> n4 (via rel_a)
        path1 = self.net.find_path(self.n1, self.n4)
        self.assertEqual(path1, [self.n1, self.n2, self.n4])

        # Path does not exist: n3 to n1
        path2 = self.net.find_path(self.n3, self.n1)
        self.assertEqual(path2, []) # Expect empty list if no path

        # Depth limitation
        path3 = self.net.find_path(self.n1, self.n4, depth=1) # n1 -> n2 (depth 1), n2 is not n4
        self.assertEqual(path3, []) # Should not find n4 within depth 1 from n1

        path_n1_n2_d1 = self.net.find_path(self.n1, self.n2, depth=1)
        self.assertEqual(path_n1_n2_d1, [self.n1, self.n2])

        # Allowed attributes
        # Path n1 -> n3 (rel_b only)
        path4 = self.net.find_path(self.n1, self.n3, allowed_attributes=["rel_b"])
        self.assertEqual(path4, [self.n1, self.n3])

        # Try finding n1 -> n4 with only rel_b (should fail)
        path5 = self.net.find_path(self.n1, self.n4, allowed_attributes=["rel_b"])
        self.assertEqual(path5, [])

        # Path with props on intermediate nodes (not directly supported by find_path, but by get_connections)
        # find_path's props param is for the connections, not intermediate nodes.

    def test_fetch_from(self):
        # Fetch all nodes reachable from n1
        # n1 -> n2 (rel_a), n1 -> n3 (rel_b), n2 -> n4 (rel_a)
        # Expected: n1, n2, n3, n4
        fetched_from_n1 = self.net.fetch_from(self.n1)
        # Order doesn't matter for fetch_from, so check contents and length
        self.assertEqual(len(fetched_from_n1), 4)
        for node in [self.n1, self.n2, self.n3, self.n4]:
            self.assertIn(node, fetched_from_n1)

        # Fetch with depth limit
        fetched_from_n1_depth1 = self.net.fetch_from(self.n1, depth=1)
        # Expected: n1, n2, n3
        self.assertEqual(len(fetched_from_n1_depth1), 3)
        self.assertIn(self.n1, fetched_from_n1_depth1)
        self.assertIn(self.n2, fetched_from_n1_depth1)
        self.assertIn(self.n3, fetched_from_n1_depth1)
        self.assertNotIn(self.n4, fetched_from_n1_depth1)

        # Fetch with allowed attributes
        fetched_from_n1_rela = self.net.fetch_from(self.n1, allowed_attributes=["rel_a"])
        # Expected: n1, n2, n4
        self.assertEqual(len(fetched_from_n1_rela), 3)
        self.assertIn(self.n1, fetched_from_n1_rela)
        self.assertIn(self.n2, fetched_from_n1_rela)
        self.assertIn(self.n4, fetched_from_n1_rela)
        self.assertNotIn(self.n3, fetched_from_n1_rela)


    def test_find_path_with_ignore_attributes(self):
        # Setup: n1 -(rel_a)-> n2 -(rel_b)-> n4
        #        n1 -(rel_c)-> n3 -(rel_d)-> n4
        # Re-setup links for clarity for this specific test
        self.n1.links = {} # Clear existing links for n1, n2, n3 for this test
        self.n2.links = {}
        self.n3.links = {}
        self.n1.commit(); self.n2.commit(); self.n3.commit()


        self.n1.link("rel_a", self.n2)
        self.n2.link("rel_b", self.n4)
        self.n1.link("rel_c", self.n3)
        self.n3.link("rel_d", self.n4)
        self.n1.commit(); self.n2.commit(); self.n3.commit()

        # Path n1 -> n2 -> n4 exists
        path_default = self.net.find_path(self.n1, self.n4)
        self.assertTrue(path_default == [self.n1, self.n2, self.n4] or path_default == [self.n1, self.n3, self.n4])


        # Ignore rel_a: path should be n1 -> n3 -> n4
        path_ignore_rela = self.net.find_path(self.n1, self.n4, ignore_attributes=["rel_a"])
        self.assertEqual(path_ignore_rela, [self.n1, self.n3, self.n4])

        # Ignore rel_b: path should be n1 -> n3 -> n4
        path_ignore_relb = self.net.find_path(self.n1, self.n4, ignore_attributes=["rel_b"])
        self.assertEqual(path_ignore_relb, [self.n1, self.n3, self.n4])

        # Ignore rel_c: path should be n1 -> n2 -> n4
        path_ignore_relc = self.net.find_path(self.n1, self.n4, ignore_attributes=["rel_c"])
        self.assertEqual(path_ignore_relc, [self.n1, self.n2, self.n4])

        # Ignore rel_d: path should be n1 -> n2 -> n4
        path_ignore_reld = self.net.find_path(self.n1, self.n4, ignore_attributes=["rel_d"])
        self.assertEqual(path_ignore_reld, [self.n1, self.n2, self.n4])

        # Ignore rel_a and rel_d: path should be blocked (n1->n3 (ok) but n3-/-reld-/-n4)
        # This means the path n1->n3->n4 is blocked.
        # The path n1->n2->n4 is also blocked if rel_a is ignored.
        # So, if we ignore rel_a and rel_d, no path.
        path_ignore_two = self.net.find_path(self.n1, self.n4, ignore_attributes=["rel_a", "rel_d"])
        self.assertEqual(path_ignore_two, [])

        path_ignore_all_blocking = self.net.find_path(self.n1, self.n4, ignore_attributes=["rel_a", "rel_c"])
        self.assertEqual(path_ignore_all_blocking, [])


    def test_fetch_from_with_ignore_attributes(self):
        # Setup: n1 -(rel_a)-> n2 -(rel_b)-> n4
        #        n1 -(rel_c)-> n3
        # Clear links for this test for clarity
        self.n1.links = {}; self.n2.links = {}; self.n3.links = {}; self.n4.links = {}
        self.n1.commit(); self.n2.commit(); self.n3.commit(); self.n4.commit()

        self.n1.link("rel_a", self.n2)
        self.n2.link("rel_b", self.n4)
        self.n1.link("rel_c", self.n3)
        self.n1.commit(); self.n2.commit()

        # Default fetch from n1: should get n1, n2, n3, n4
        # (Assuming n4 is reachable from n2 if n2.commit() is effective)
        # The self.net.append_all was done in setUp.
        # The links made here are on node instances that are part of the net.

        all_fetched = self.net.fetch_from(self.n1)
        self.assertIn(self.n1, all_fetched)
        self.assertIn(self.n2, all_fetched)
        self.assertIn(self.n3, all_fetched)
        self.assertIn(self.n4, all_fetched) # n4 is reachable via n2
        self.assertEqual(len(all_fetched), 4)

        # Ignore rel_a: n2 and n4 should not be fetched via rel_a path
        # Should get n1, n3
        fetched_ignore_rela = self.net.fetch_from(self.n1, ignore_attributes=["rel_a"])
        self.assertIn(self.n1, fetched_ignore_rela)
        self.assertIn(self.n3, fetched_ignore_rela)
        self.assertNotIn(self.n2, fetched_ignore_rela)
        self.assertNotIn(self.n4, fetched_ignore_rela) # n4 only reachable via n2 which uses rel_a from n1
        self.assertEqual(len(fetched_ignore_rela), 2)

        # Ignore rel_b: n4 should not be fetched if rel_b is the only way to it from n2
        # Should get n1, n2, n3
        fetched_ignore_relb = self.net.fetch_from(self.n1, ignore_attributes=["rel_b"])
        self.assertIn(self.n1, fetched_ignore_relb)
        self.assertIn(self.n2, fetched_ignore_relb)
        self.assertIn(self.n3, fetched_ignore_relb)
        self.assertNotIn(self.n4, fetched_ignore_relb)
        self.assertEqual(len(fetched_ignore_relb), 3)

        # Ignore rel_c: n3 should not be fetched
        # Should get n1, n2, n4
        fetched_ignore_relc = self.net.fetch_from(self.n1, ignore_attributes=["rel_c"])
        self.assertIn(self.n1, fetched_ignore_relc)
        self.assertIn(self.n2, fetched_ignore_relc)
        self.assertIn(self.n4, fetched_ignore_relc)
        self.assertNotIn(self.n3, fetched_ignore_relc)
        self.assertEqual(len(fetched_ignore_relc), 3)


    def test_to_graphviz_output(self):
        gv_net = Net("GraphVizTestNet")
        n1 = Node("gv_n1", props={"role": "source"}, type="root")
        n2 = Node("gv_n2", props={"status": "active"})
        n3 = Node("gv_n3", type="leaf")
        n_parent = Node("gv_parent")
        n_child = Node("gv_child")

        gv_net.append_all([n1, n2, n3, n_parent, n_child])

        n1.link("connects_to", n2, power=5, mode=1)
        n2.link("related_to", n3, power=2, mode=0) # Negative link
        n_child.extends(n_parent)

        # Commit links to ensure they are static for graphviz generation
        n1.commit()
        n2.commit()
        n_child.commit() # commit child to process extends relationship static links

        dot_output = gv_net.to_graphviz()

        # Basic checks for DOT syntax and content
        self.assertTrue(dot_output.startswith("digraph SemaWalNetwork {"))
        self.assertTrue(dot_output.endswith("}"))
        self.assertIn("rankdir=LR;", dot_output)

        # Check node declarations (names might be quoted)
        self.assertIn('"gv_n1" [label="gv_n1\\n(Type: root)\\nProps: role: source"', dot_output)
        self.assertIn("shape=box", dot_output)
        self.assertIn("color=lightcoral", dot_output)


        self.assertIn('"gv_n2" [label="gv_n2\\n(Type: regular)\\nProps: status: active"', dot_output)

        self.assertIn('"gv_n3" [label="gv_n3\\n(Type: leaf)"', dot_output) # Leaf node might not have props in this test
        self.assertIn("shape=octagon", dot_output)
        self.assertIn("color=lightgreen", dot_output)

        # Check edge declarations
        self.assertIn('"gv_n1" -> "gv_n2" [label="connects_to (P:5)", color=darkgreen];', dot_output)
        self.assertIn('"gv_n2" -> "gv_n3" [label="related_to (P:2)", color=red, style=dashed];', dot_output)

        # Check extends relationship
        self.assertIn('"gv_child" -> "gv_parent" [label="extends", style=dotted, arrowhead=onormal, color=blue];', dot_output)

        # Check if parent and child are declared (their labels might be simpler if no specific props/type styling was hit for them)
        self.assertIn('"gv_parent" [label="gv_parent\\n(Type: regular)', dot_output)
        self.assertIn('"gv_child" [label="gv_child\\n(Type: regular)', dot_output)

        # Optional: print for manual inspection if tests fail
        # print("\n--- DOT Output ---")
        # print(dot_output)
        # print("--- End DOT Output ---")


if __name__ == '__main__':
    unittest.main()
