from node import Node
from net import Net
from csv_parser import parser
import re

n = parser.read("net.csv")

print("")


# n1 = Node("node_1")
# n2 = Node("node_2")
# n3 = Node("node_3")
# n4 = Node("node_4")

# n1.link("is", n2, 1, 1)
# n2.link("is", n3, 1, 1)
# n3.link("is", n4, 0, 1)
# n4.link("is", n1, 1, 1)

# n = Net("test_net")
# n.add(n1)
# n.add(n2)
# n.add(n3)
# n.add(n4)
# n1.link("has", n)
# n.randomSearch()



# print("------------- node 1")
# n1.showLinks()
# print("------------- node 2")
# n2.showLinks()
# print("------------- node 3")
# n3.showLinks()
# print("------------- node 4")
# n4.showLinks()
# print("------------- relations")
# print(n3.relationsWith(n2))
# print("------------- connections")
# print(n3.connections())
# print("------------- answer")
# print("is:", n3.answer("is", n2, 0))

# net = parser.read("net.csv")
# net.randomSearch()

# n = net.getNode("node_1")
# print("------------- node 1")
# n.showLinks()
# print("------------- node test")

# n1 = Node("test")
# n1.extend(n)
# n1.showLinks()
# print("------------- after the ")
# n.link("is_a", net.getNode("node_4"))
# n1.showLinks()
# rr = n1.r()
# print()



# defining the nodes
# grandfather_A = Node("Grandfather A")
# grandmother_A = Node("Grandmother A")
# parent_A = Node("Parent A")

# grandfather_B = Node("Grandfather B")
# grandmother_B = Node("Grandmother B")
# parent_B = Node("Parent B")

# parent_C = Node("Parent C")

# child_1 = Node("Child 1")
# child_2 = Node("Child 2")
# child_3 = Node("Child 3")
# child_4 = Node("Child 4")

# killer = Node("Killer")

# declaring the relations between the nodes
# grandfather_A.mutual_link("Maried to", grandmother_A)

# grandfather_A.link("Parent of", parent_A)
# grandmother_A.link("Parent of", parent_A)
# parent_A.link("Child of", grandfather_A)
# parent_A.link("Child of", grandmother_A)

# grandfather_B.mutual_link("Maried to", grandmother_B)

# grandfather_B.link("Parent of", parent_B)
# grandmother_B.link("Parent of", parent_B)
# parent_B.link("Child of", grandfather_B)
# parent_B.link("Child of", grandmother_B)

# parent_A.link("Parent of", child_1)
# parent_A.link("Parent of", child_2)
# parent_A.link("Parent of", child_3)

# parent_B.link("Parent of", child_1)
# parent_B.link("Parent of", child_2)
# parent_B.link("Parent of", child_3)

# child_1.link("Child of", parent_A)
# child_1.link("Child of", parent_B)
# child_2.link("Child of", parent_A)
# child_2.link("Child of", parent_B)
# child_3.link("Child of", parent_A)
# child_3.link("Child of", parent_B)

# parent_C.link("Parent of", child_4)
# child_4.link("Child of", parent_C)

# child_1.mutual_link("Sibling to", child_2)
# child_1.mutual_link("Sibling to", child_3)
# child_2.mutual_link("Sibling to", child_3)

# the drama
# parent_A.mutual_link("Divorced", parent_B)

# parent_A.mutual_link("Maried to", parent_C)

# grandfather_A.link("Hates", parent_A)
# grandmother_A.link("Hates", parent_A)
# parent_B.mutual_link("Hates", parent_A)
# grandfather_B.link("Hates", parent_A)
# grandmother_B.link("Hates", parent_A)

# child_2.link("Hates", child_1)

# irrelevant drama
# killer.link("Killed", child_1)
# child_3.link("Wants to kill", killer)

# testing node functions
# print("|------------------------------------------------------------|")
# print("Showing all the relations with Parent A:")
# parent_A.showLinks()
# print("|------------------------------------------------------------|")
# print("Showing all the relations between Parent A and Parent B:")
# print(parent_A.relationsWith(parent_B))
# print("|------------------------------------------------------------|")
# print("Answering a given question:")
# print("Does Grandfather A likes his child: ", grandfather_A.answer("Like", parent_A))
# print("Does Grandfather A hates his child: ", grandfather_A.answer("Hates", parent_A))
# print("|------------------------------------------------------------|")


# testing network functions
# defining the networks
# small_familly = Net()
# big_familly = Net()

# adding nodes to networks
# small_familly.add(parent_A)
# small_familly.add(parent_B)
# small_familly.add(parent_C)
# small_familly.add(child_1)
# small_familly.add(child_2)
# small_familly.add(child_3)
# small_familly.add(child_4)


# big_familly.add(grandfather_A)
# big_familly.add(grandmother_A)
# big_familly.add(grandfather_B)
# big_familly.add(grandmother_B)

# big_familly.add(parent_A)
# big_familly.add(parent_B)
# big_familly.add(parent_C)
# big_familly.add(child_1)
# big_familly.add(child_2)
# big_familly.add(child_3)
# big_familly.add(child_4)

# big_familly.add(killer)

# testing network functions
# small_familly.random_search()
# big_familly.search(parent_A, depth=2)
# print("Grandfather A related to child 1 by parenting relation: ", big_familly.isLinkedBy(grandfather_A, "Parent of", child_4))
# print("Grandfather A related to child 4 by parenting relation: ", big_familly.isLinkedBy(grandfather_A, "Parent of", child_4))
# big_familly.drawPath(killer, child_4)