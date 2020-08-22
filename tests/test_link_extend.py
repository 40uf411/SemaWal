import sys

import argparse

import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    
from semawal.node import Node

n1 = Node(name="Node 1", props={"p1": "v1", "p2": "v2"}, type="root")
n2 = Node(name="Node 2")
n3 = Node("Node 3")
n4 = Node(name="Node 4")
print("Phase 1 #############################################")
n3.extends(n1)
n3.link(attribute="test", node=n2, power=3)
n1.link(attribute="test", node=n2, power=5)
n3.showLinks()
print("Phase 2 #############################################")
n3.link(attribute="test", node=n2, power=7)
#n1.reset()
#n3.reset()
n3.showLinks()
print("Phase 3 #############################################")
n1.extends(n4)
n4.link("is_a", n2)
n3.showLinks()