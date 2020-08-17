# SemaWal Semantic network resolver
SemaWal is a semantic network resolver in python

<!--![arrand logo](doc/arrand_header.png  "arrand logo")-->
<!--![PyPI - Downloads](https://img.shields.io/pypi/dm/arrand)-->

  Developper:  Ali AOUF

Features |   value
---------|---------------------------------------------------------------------------------
Authors  | [Authors.md](https://github.com/40uf411/SemaWal/master/AUTHORS.md)
Release  | 0.1
License  |[Apache 2.0](https://github.com/40uf411/SemaWal/master/LICENSE)
Tracker  |[40uf411/arrand/Issues](https://github.com/40uf411/SemaWal/issues)
Source  |[Github](http://github.com/40uf411/SemaWal)
Feedbacks  |[Comments](https://github.com/40uf411/SemaWal/)
Accounts  |[@Twitter](https://twitter.com/40uf411))

## Description

SemaWal Is a semantic network resolver developed as a python library. It allows the creation of networks through manual coding or a CSV file. It supports many types of connections between nodes.
In addition to extracting knowledge (mainly relations) between two or more nodes in a network, it can find paths between nodes in a given network.

###  Features:
* Support for multi-relations(connections between nodes).
* Support for three types of relations: Strict, regular, extend(inheritance).
* Support for positive and negative relations.
* Support for CSV files.
* Support for Sub-networks.
* Node functions:
	* Fetch all the related nodes and all the relations that a given node has. 
	* Fetch nodes that are related to a given node.	
	* Fetch relations that relate two given nodes has.
	* Fetch all the relations that a network contains.
	* Fetch all the relations you can get starting from a given node until reaching a given depth.
	* Check if two given nodes are directly connected by a given relation.
	* Check if two given nodes are connected through a path of nodes.
	* Check if two given nodes are connected through a path of nodes by a given relation.
	* Draw a path between two given nodes.

### Usage
<!--
### install
```shell
pip install arrand
```
#### [requirement]
```
pyarabic>=0.6.8
```
-->
#### import
```python
>>> from node import Node
>>> from net import Net
>>> from csv_parser import parser
```
## Examples

Detailed examples and features in [test.py](test.py) 

*  Creating nodes
```python
>>> nodeA = Node(name="A")
[!] Created node A
>>> nodeB = Node(name="B")
[!] Created node B
>>> nodeC = Node(name="C")
[!] Created node C
```

*  Linking two nodes
```python
>>> ## One-way relation: Ex: A has B
>>> # mode (int): 0=negative, 1=positive
>>> # power (int): 0=none strict, 1=strict
>>> nodeA.link(attribute="has", node=NodeB, mode=1, power=1)
>>> ## Mutual Link: Ex: A is B and B is A
>>> nodeA.mutual_link(attribute="is", node=NodeB, mode=1, power=1)
>>> ## Inheritance (A inherits B relations): Ex: A extends B
>>> nodeA.extends(node=NodeC)
```

* Node functions
```python
>>> ## Return all the nodes that are connected to a given node.
>>> # all (boolean): consider negative relation(relations with mode=0) like "is not", "has not"... 
>>> nodeA.connections(all=true)
{<node.Node object at 0x7ff0d8d32310>, <node.Node object at 0x7ff0d8cfcfd0>}
>>> ## Return relations with a given node
>>> nodeA.relationsWith(node=nodeB)
['is']
>>> ## Print all the relations that a node has
>>> nodeA.showLinks()
A       |   is  |   B  mode:  1  strict:  1
A       |   extends     |   C  mode:  1  strict:  1
>>> ## Check if there is a direct relation between two nodes
>>> nodeA.check(attribute="is", node=nodeB, mode=1)
True
```

*  Creating a network
```python
>>> myNet = Net(name="MyNet")
[!] Created network MyNet
```

*  Importing a network from a csv file
```python
>>> n = parser.read("link_test.csv")
[!] Created network  link_test
```

*  Adding a node to a network
```python
>>> myNet.add(nodeA, nodeB, nodeC)
```

*  Get a node from a network
```python
>>> myNet.getNode("A")
```

*  Get a list of all the nodes in a network
```python
>>> myNet.getNodeskeys()
['A', 'B', 'C']
```

*  Fetching all the relations in a network
```python
>>> myNet.randomSearch()
A       |   is  |   B  mode:  1  strict:  1
A       |   extends     |   C  mode:  1  strict:  1
B       |   is  |   A  mode:  1  strict:  1
```

*  Fetching all the relations in a starting from a giving node until reaching a given depth
```python
>>> myNet.search(node=nodeB, depth=3)
B       |   is  |   A  mode:  1  strict:  1
A       |   is  |   B  mode:  1  strict:  1
A       |   extends     |   C  mode:  1  strict:  1
```

* Get the path that relats two nodes
```python
>>> myNet.areConnected(nodeA=nodeA, nodeB=nodeB)
B       |   is  |   A  mode:  1  strict:  1
A       |   is  |   B  mode:  1  strict:  1
[<node.Node object at 0x7f0571bbb4c0>, <node.Node object at 0x7f0571ac2310>]
>>> # that was [nodeA, nodeB]
```

* Printing the path that relats two nodes
```python
>>> myNet.drawPath(nodeA=nodeA, nodeB=nodeB)
Printing the path:
A       |   ['is']      |   B
```

### On progress features
* A GUI interface
* Nodes properties
* An option to ignore certain relations
