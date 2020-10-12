import sys

import argparse

import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    
#importing classes
from semawal.node import Node
from semawal.net import Net
# Level 0
n0 = Node("0")
# Level 1
n1_0 = Node("1_0")
n1_1 = Node("1_1")
n0.link("test0", n1_0)
n0.link("test1", n1_1)
# Level 2
n2_0 = Node("2_0")
n2_1 = Node("2_1")
n1_0.link("test0", n2_0)
n1_0.link("test1", n2_1)

n2_2 = Node("2_2")
n2_3 = Node("2_3")
n1_1.link("test0", n2_2)
n1_1.link("test1", n2_3)
# Level 3
n3_0 = Node("3_0")
n3_1 = Node("3_1")
n2_0.link("test0", n3_0)
n2_0.link("test1", n3_1)

n3_2 = Node("3_2")
n3_3 = Node("3_3")
n2_1.link("test0", n3_2)
n2_1.link("test1", n3_3)

n3_4 = Node("3_4")
n3_5 = Node("3_5")
n2_2.link("test0", n3_4)
n2_2.link("test1", n3_5)

n3_6 = Node("3_6")
n3_7 = Node("3_7")
n2_3.link("test0", n3_6)
n2_3.link("test1", n3_7)

# Test
print("#"*20, "test")
t=n0.checkPattern([
    {
        "num":-1,
        "attributes": ["test1"],
        "props": {},
        "mode": -1,
        "minPower": 0,
        "maxPower":10
    }
])
print("t= ", t)
# pattern = [
#     {
#         "num": 5,
#         "attributes": ["Test"],
#         "props": {
#             "p1": [["<", 10], [">", 9]]
#         },
#         "mode": -1,
#         "minPower": 0,
#         "maxPower": 10
#     }
# ]
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

# from semawal.json_parser import Parser
# print("exporting -------------------------")
# Parser.export(nt, "test.json")

# net = Parser.read("test.json")
# net.showLinks()
# print(net.getNode("1").getProperties())
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