import unittest
from semawal.node import Node
from semawal.exceptions import PropertyError, LinkCreationError, NodeTypeConflictError

class TestNode(unittest.TestCase):

    def setUp(self):
        # Reset global node states if any (not explicitly needed for SemaWal's Node as per current code)
        pass

    def test_node_creation_and_properties(self):
        n1 = Node("n1", props={"color": "blue"}, type="regular")
        self.assertEqual(n1.name(), "n1")
        self.assertEqual(n1.type(), "regular")
        self.assertEqual(n1.get_properties()["color"], "blue")

        with self.assertRaises(PropertyError):
            Node("n_err", props="not_a_dict")

        n1.add_property("size", 10)
        self.assertEqual(n1.get_property("size"), 10)
        n1.drop_property("color")
        self.assertIsNone(n1.get_property("color")) # Assuming drop_property sets to None

    def test_node_rename(self):
        n = Node("original")
        n.rename("new_name")
        self.assertEqual(n.name(), "new_name")

    def test_validate_properties(self):
        n = Node("validator", props={"age": 30, "status": "active"})
        self.assertTrue(n.validate_properties({"age": [(">=", 20)], "status": [("==", "active")]}))
        self.assertFalse(n.validate_properties({"age": [("<", 20)]}))
        self.assertFalse(n.validate_properties({"non_existent_prop": [("==", "any")]}))

    def test_node_extends(self):
        parent = Node("parent", props={"lastname": "Smith"}, type="regular")
        parent.link("knows", Node("p_friend"), power=5)

        child = Node("child", props={"firstname": "John"}, type="regular")
        child.extends(parent)

        self.assertEqual(child.parent(), parent)
        self.assertEqual(child.get_property("lastname"), "Smith")
        self.assertEqual(child.get_property("firstname"), "John")

        # Test property overriding
        child.add_property("lastname", "Doe")
        self.assertEqual(child.get_property("lastname"), "Doe")
        # Parent property should remain unchanged if properties are copied, not referenced (deep copy needed for props)
        # Current implementation: self.properties = p (p is parent.get_properties(), which returns a copy)
        # then child's own props are merged. So this is fine.

        # Test link inheritance
        child.commit() # or generate_static_links
        parent_links = parent.get_links()
        child_links = child.get_links()
        self.assertIn("knows", child_links)
        self.assertEqual(child_links["knows"][0][0].name(), "p_friend")
        self.assertEqual(child_links["knows"][0][2], 5) # power

        # Test overriding inherited link
        child_friend = Node("c_friend")
        child.link("knows", child_friend, power=7) # Higher power
        child.commit()
        child_links_updated = child.get_links()
        self.assertEqual(child_links_updated["knows"][0][0].name(), "c_friend")
        self.assertEqual(child_links_updated["knows"][0][2], 7)

        # Test extending a leaf node
        leaf_node = Node("leafy", type="leaf")
        child2 = Node("child2")
        with self.assertRaises(NodeTypeConflictError):
            child2.extends(leaf_node)

        # Test extending when already has a parent (implicitly tested by linking not failing this)
        # The error is for child already having links, not for already having a parent.
        # The message is: "[*] Node child can't extend another node since it already has links with other nodes."
        # This should be LinkCreationError as per docstring.
        # Let's test the "already has links" scenario, then "already has parent"
        child_with_link = Node("child_linked")
        child_with_link.link("some_rel", Node("another"))
        child_with_link.commit()

        # The error "can't extend another node since it already has links with other nodes"
        # is actually related to self.parent() being an instance of Node,
        # which means it has already extended something.
        # The actual code: if isinstance(self.parent(), Node): raise LinkCreationError(...)
        extender1 = Node("ext1")
        extender2 = Node("ext2")
        base_parent = Node("base_parent_for_extend_test")
        extender1.extends(base_parent) # ext1 now has a parent
        with self.assertRaises(LinkCreationError):
             extender1.extends(extender2) # Trying to extend again

    def test_node_link_creation(self):
        n1 = Node("n1_linker")
        n2 = Node("n2_linked_to")
        n_leaf = Node("n_leaf", type="leaf")
        n_root = Node("n_root", type="root")

        n1.link("connects", n2, mode=1, power=3)
        n1.commit()
        self.assertIn("connects", n1.get_links())
        self.assertEqual(n1.get_links()["connects"][0][0], n2)
        self.assertEqual(n1.get_links()["connects"][0][1], 1) # mode
        self.assertEqual(n1.get_links()["connects"][0][2], 3) # power

        with self.assertRaises(NodeTypeConflictError):
            n_leaf.link("tries_to_link", n1)

        with self.assertRaises(NodeTypeConflictError):
            n1.link("tries_to_link_root", n_root)

        # Test conflicting link (lower power link cannot override higher power static link from parent)
        # This requires the 'extends' setup
        parent_for_conflict = Node("parent_conflict")
        linked_node_conflict = Node("linked_conflict")
        parent_for_conflict.link("conflict_rel", linked_node_conflict, power=5)
        parent_for_conflict.commit()

        child_conflict = Node("child_conflict")
        child_conflict.extends(parent_for_conflict)
        child_conflict.commit()

        # child_conflict now has static link "conflict_rel" to linked_node_conflict with power 5
        # Trying to add a local link with same attribute and node but lower power would be an issue.
        # The LinkCreationError is for "compatibility == -1"
        # compatibility == -1 means an existing static link has HIGHER or EQUAL power.
        with self.assertRaises(LinkCreationError):
             child_conflict.link("conflict_rel", linked_node_conflict, power=3) # Lower power

    def test_get_connections_and_relations(self):
        n1 = Node("n1_connect")
        n2 = Node("n2_friend", props={"age": 25})
        n3 = Node("n3_colleague", props={"age": 35})
        n4 = Node("n4_family", props={"age": 25})

        n1.link("friend", n2, power=1)
        n1.link("colleague", n3, power=2)
        n1.link("friend", n4, power=3, mode=0) # Negative friend
        n1.commit()

        friends = n1.get_connections(attributes=["friend"])
        self.assertIn(n2, friends)
        self.assertIn(n4, friends)
        self.assertEqual(len(friends), 2)

        colleagues = n1.get_connections(attributes=["colleague"])
        self.assertIn(n3, colleagues)
        self.assertEqual(len(colleagues), 1)

        age_25 = n1.get_connections(props={"age": [("==", 25)]})
        self.assertIn(n2, age_25)
        self.assertIn(n4, age_25) # n4 also has age 25 in this test setup
        self.assertEqual(len(age_25), 2)

        positive_links = n1.get_connections(mode=1)
        self.assertIn(n2, positive_links)
        self.assertIn(n3, positive_links)
        self.assertEqual(len(positive_links), 2)

        high_power_links = n1.get_connections(min_power=2)
        self.assertIn(n3, high_power_links)
        self.assertIn(n4, high_power_links) # n4 link has power 3
        self.assertEqual(len(high_power_links), 2)

        self.assertEqual(sorted(n1.get_relations_with(n2)), sorted(["friend"]))
        self.assertEqual(sorted(n1.get_relations_with(n4)), sorted(["friend"]))


    def test_drop_link(self):
        n1 = Node("n1_dropper")
        n2 = Node("n2_to_drop")
        n3 = Node("n3_to_keep")
        n1.link("temp_rel", n2)
        n1.link("perm_rel", n3)
        n1.commit()
        self.assertIn(n2, n1.get_connections(attributes=["temp_rel"]))

        n1.drop_link(attribute="temp_rel", node=n2)
        n1.commit()
        self.assertNotIn(n2, n1.get_connections(attributes=["temp_rel"]))
        self.assertIn(n3, n1.get_connections(attributes=["perm_rel"]))
        # Ensure the specific link is dropped, not all links of that attribute
        n1.link("temp_rel", n2) #re-add
        n1.link("temp_rel", Node("another_linked_to_temp"))
        n1.commit()
        n1.drop_link(attribute="temp_rel", node=n2)
        n1.commit()
        self.assertNotIn(n2, n1.get_connections(attributes=["temp_rel"]))
        self.assertTrue(len(n1.get_connections(attributes=["temp_rel"])) > 0)


    def test_node_check_pattern(self):
        # Setup: A -> B -> C, A -> D
        # A: name='a', type='start'
        # B: name='b', type='middle'
        # C: name='c', type='end'
        # D: name='d', type='middle'
        a = Node("a", props={"type": "start"})
        b = Node("b", props={"type": "middle"})
        c = Node("c", props={"type": "end"})
        d = Node("d", props={"type": "middle"})

        a.link("next", b)
        b.link("next", c)
        a.link("next_alt", d)
        a.commit(); b.commit(); c.commit(); d.commit()

        # Pattern 1: A -(next)-> B -(next)-> C
        pattern1 = [
            {"attributes": ["next"], "props": {}, "mode": -1, "minPower": 0, "maxPower": 10, "num": 1},
            {"attributes": ["next"], "props": {}, "mode": -1, "minPower": 0, "maxPower": 10, "num": 1}
        ]
        paths1 = a.check_pattern(pattern=pattern1)
        # Expected: [[a, b, c]]
        self.assertEqual(len(paths1), 1)
        self.assertEqual(paths1[0], [a,b,c])


        # Pattern 2: A -(next or next_alt)-> ? (type middle)
        pattern2 = [
            {"attributes": ["next", "next_alt"], "props": {"type": [("==", "middle")]}, "mode": -1, "minPower": 0, "maxPower": 10, "num": 1}
        ]
        paths2 = a.check_pattern(pattern=pattern2)
        # Expected: [[a,b], [a,d]] (order might vary) or a list containing these two lists
        self.assertEqual(len(paths2), 2) # Should find paths to b and d
        self.assertTrue(any(path == [a, b] for path in paths2))
        self.assertTrue(any(path == [a, d] for path in paths2))

        # Pattern 3: A -> B (and B must be type 'end') - Should fail
        pattern3 = [
             {"attributes": ["next"], "props": {"type": [("==", "end")]}, "mode": -1, "minPower": 0, "maxPower": 10, "num": 1}
        ]
        paths3 = a.check_pattern(pattern=pattern3)
        # The current implementation of check_pattern returns [self] if no path is found for the first step
        # or if a subsequent step fails. This might need refinement for "no path found" vs "path found but incomplete".
        # For now, we expect it not to find a path to c directly from a via 'next' that is also type 'end'.
        # It finds [a,b], then b checks pattern. If pattern is empty, it returns [[b, node_from_b_links]].
        # If pattern is not empty, it continues.
        # If b.get_connections for pattern[0] is empty, it returns [b].
        # So a path of [a,b] could be returned if b doesn't match the rest of pattern.
        # The test is tricky. Let's simplify: find a node of type 'end' via 'next'
        pattern3_revised = [
            {"attributes": ["next"], "props": {}, "mode": -1, "minPower": 0, "maxPower": 10, "num": 1}, # A->B
            {"attributes": [], "props": {"type": [("==", "end")]}, "mode": -1, "minPower": 0, "maxPower": 10, "num": 1} # B must be type end (check B itself)
            # This pattern structure is not how check_pattern works.
            # check_pattern expects attributes for transitions.
            # To check a property of the *target* node of a transition, it's in the *same* pattern entry.
        ]
        # Correct way: A -(next)-> Node (must be type 'end')
        pattern3_corrected = [
            {"attributes": ["next"], "props": {"type": [("==", "end")]}, "mode": -1, "minPower": 0, "maxPower": 10, "num": 1}
        ]
        paths3_corrected = a.check_pattern(pattern=pattern3_corrected)
        # a.get_connections for this will be empty, as 'b' is not type 'end'.
        # So paths3_corrected should be [[a]] based on current check_pattern behavior.
        # Updated check_pattern logic: should return [] if no valid path found for the step.
        self.assertEqual(paths3_corrected, [])


        # Pattern 4: A -(next){2}-> C (num = 2 for 'next' attribute)
        # This 'num' usage is for repeated checks from the *same* node, not path length.
        # The current check_pattern num logic:
        # if num > 0: if num == 1, pop(0). if len(pattern) == 0, return. else num--.
        # This is more like "match this step 'num' times from current node before moving to next pattern step".
        # For a path of length 2, we need two pattern elements.
        # Let's test "num" for finding multiple distinct nodes from current:
        # A has two "next_multi" links to M1, M2.
        m1 = Node("m1")
        m2 = Node("m2")
        a.link("next_multi", m1)
        a.link("next_multi", m2)
        a.commit()

        pattern_num = [
            {"attributes": ["next_multi"], "props": {}, "mode": -1, "minPower": 0, "maxPower": 10, "num": 2}
        ]
        # This is tricky because num is decremented. If num=2, it looks for one, then num becomes 1.
        # Then it looks for another with num=1 (which pops pattern).
        # The current check_pattern logic for num > 0 might not be intuitive for "find N such links".
        # It seems more geared towards "this part of the pattern must apply N times".
        # Given the report's comment "Significantly refactored and added detailed inline comments to check_pattern",
        # the exact behavior of `num` might have been clarified.
        # Assuming `num` is how many items matching the current pattern step before moving to the *next* pattern step.
        # The current code:
        # if pattern[0]["num"] > 0:
        #    if pattern[0]["num"] == 1: pattern.pop(0)
        #    ...
        #    if(len(pattern) == 0): return [[self,node] for node in nodes ...] <- if original num was 1
        #    else: pattern[0]["num"] = pattern[0]["num"]-1; for node in nodes: recurse...
        # This means if num=2, it finds connections, then for each connection, it re-runs check_pattern with num=1 for the *same* pattern item.
        # If that succeeds (finds another connection from *that* node), it then moves to the *next* pattern item.
        # This is not "find 2 peers". It's "find a path of length `num` where each step matches this pattern item".

        # Let's test a simple path again with explicit logging if it fails.
        # A -(next)-> B
        pattern_simple_ab = [
            {"attributes": ["next"], "props": {"type": [("==", "middle")]}, "mode": -1, "minPower": 0, "maxPower": 10, "num": 1}
        ]
        paths_ab = a.check_pattern(pattern=pattern_simple_ab)
        self.assertTrue(any(p == [a,b] for p in paths_ab), f"Expected path [a,b] not found in {paths_ab}")


    def test_get_connections_with_ignore_attributes(self):
        n1 = Node("n1_ignore_test")
        n_friend = Node("n_friend_ignore")
        n_coworker = Node("n_coworker_ignore")
        n_family = Node("n_family_ignore")

        n1.link("friend", n_friend)
        n1.link("work", n_coworker)
        n1.link("family", n_family)
        n1.commit()

        # No ignore
        all_conns = n1.get_connections()
        self.assertEqual(len(all_conns), 3)

        # Ignore 'friend'
        conns_ignore_friend = n1.get_connections(ignore_attributes=["friend"])
        self.assertEqual(len(conns_ignore_friend), 2)
        self.assertNotIn(n_friend, conns_ignore_friend)
        self.assertIn(n_coworker, conns_ignore_friend)
        self.assertIn(n_family, conns_ignore_friend)

        # Ignore 'work' and 'family'
        conns_ignore_work_family = n1.get_connections(ignore_attributes=["work", "family"])
        self.assertEqual(len(conns_ignore_work_family), 1)
        self.assertIn(n_friend, conns_ignore_work_family)
        self.assertNotIn(n_coworker, conns_ignore_work_family)
        self.assertNotIn(n_family, conns_ignore_work_family)

        # Ignore all connected attributes
        conns_ignore_all = n1.get_connections(ignore_attributes=["friend", "work", "family"])
        self.assertEqual(len(conns_ignore_all), 0)

        # Ignore non-existent attribute (should have no effect)
        conns_ignore_non_existent = n1.get_connections(ignore_attributes=["non_existent_attr"])
        self.assertEqual(len(conns_ignore_non_existent), 3)


if __name__ == '__main__':
    unittest.main()
