import sys

import argparse

import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    
#importing classes
from semawal.node import Node
from semawal.net import Net
# n1 = Node("1", type="root", props={"p":1, "p2": 2})
# n2 = Node("2")
# n3 = Node("3")
# n4 = Node("4")

# n4.extends(n3)
# n3.extends(n2)
# n2.extends(n1)

# n1.link("test", n2)
# n2.link("test", n3)
# n3.link("test", n4)

#n4.showLinks()


# nt = Net()
# nt.appendAll([n1, n2, n3, n4])

# nt.link("test", n1)
# #nt.showLinks()
# print(nt.fetchFrom(n1, depth=2, allowedAttributes=['test']))

from semawal.json_parser import Parser
# print("exporting -------------------------")
# Parser.export(nt, "test.json")

net = Parser.read("test.json")
net.showLinks()
print(net.getNode("1").getProperties())
# n = Node("node", props={
#     "p1": 5,
#     "p2": 10,
#     "p3": "hi"
# })
# print(n.properties)
# p = {
#     "p1": [["<", 10], [">", 9]]
# }
# v = n.validateProp(p)
# print(v)



# n = Node(
#     name="My node", 
#     props={"type":"name", "position":1},
#     type="root")
# n.rename("test node")

# n1 = Node(name="Node 1", props={"p1": "v1", "p2": "v2"}, type="root")
# n2 = Node(name="Node 2")
# n3 = Node("Node 3")
# n4 = Node(name="Node 4")

# n4.link("h1", n1, power=7)
# n4.link("h2", n2, mode=0)
# n4.link("h3", n3)
# print(n4.getConnections(attributes=["h1"], minPower=5))
# print(n4.getLinksAttributes())
# print(n4.getRelationesWith(n1))
# n4.showLinks()
# #######################################################################################"

# print("Phase 1 #############################################")
# n3.extends(n1)
# n3.link(attribute="test", node=n2, power=3)
# n1.link(attribute="test", node=n2, power=5)
# n3.showLinks()
# print("Phase 2 #############################################")
# n3.link(attribute="test", node=n2, power=7)
# #n1.reset()
# #n3.reset()
# n3.showLinks()
# print("Phase 3 #############################################")
# n1.extends(n4)
# n4.link("is_a", n2)
# n3.showLinks()