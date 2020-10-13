# SemaWal Semantic network resolver
<div style="text-align:center">
<img src="logo.png" alt="SemaWal logo" style="width:250px;"/>
</div>
SemaWal is a semantic network resolver in python

<!--![arrand logo](doc/arrand_header.png  "arrand logo")-->
<!--![PyPI - Downloads](https://img.shields.io/pypi/dm/arrand)-->

  Developper:  Ali AOUF

Features |   value
---------|---------------------------------------------------------------------------------
Authors  | [Authors.md](https://github.com/40uf411/SemaWal/master/AUTHORS.md)
Release  | 0.2 (20.10)
License  |[GPL](https://github.com/40uf411/SemaWal/master/LICENSE)
Tracker  |[40uf411/arrand/Issues](https://github.com/40uf411/SemaWal/issues)
Source  |[Github](http://github.com/40uf411/SemaWal)
Feedbacks  |[Comments](https://github.com/40uf411/SemaWal/)
Accounts  |[@Twitter](https://twitter.com/40uf411)

## **Description**

SemaWal Is a semantic network resolver developed as a python library. 
It allows the creation of networks through manual coding or a JSON file. It supports a variety of connection types between nodes.
SemaWal provides useful network defining functions and knowledge extraction functions, these functions allows for network browsing, path finding, pattern checking and more.

###  Features:
* Support for multi-relations(connections between nodes).
* Support for extend relation(inheritance).
* Support for positive and negative relations.
* Support for JSON files.
* Support for node properties.
* Support for Sub-networks.
* Relations extraction.
* Pattern checking.
* Advanced filtered search.
* Path finding.
* Static graph generation.
---
### Changelog:
#### 0.2(20.10)
	- New code (Node and Net classes rewritten from scratch)
	- Allowing power value to be and integer between 0 and 10 (old: 0 or 1)
	- Adding JSON support
	- Adding a function to look for pattern (Beta)
	- Deprecating the CSV parser
	- Deprecating the tkinter based GUI
#### 0.1(20.08)
	- initial release
### In progress features
* A GUI interface
* An option to ignore certain relations

---
### Usage
### install
```shell
pip install semawal
```
#### [requirement]
SemaWal 0.2 requires no lib 😉️😊️
```
```

#### import
```python
>>> from semawal.node import Node
>>> from semawal.net import Net
>>> from semawal.csv_parser import parser
```
---
### SemaWal Node object
A node is the essential building block of a semantic network. A SemaWal node has a name, a type, and it can have a list of properties. A SemaWal node can extend another node, which will give it a copy of the parent node links.
When linking two nodes, SamaWal saves the link on the node that is considered the start of the link.
 In order to accelerate operations on the links, SemaWal stores the links in a local hidden node attribute,  and it generates a list of links that includes all the local links as well as the parent node links. This process will reduce the number of links calculation and thus accelerate operations like searching and tracking.
To use the Node you have to import the Node class as the following:
```python
from semawal.node import Node
```
#### Create a node
```python
Node(name, props={}, type="regular")
```
Creating a Node is as simple as calling the default constructor. It takes as input the name of the node, its parameters and, its type.
There are three types of nodes:
  * **root:** can create links leading to other nodes, but no node can create link leading to a root node.
  * **regular:** a normal node.
  * **leaf:** can't create any link. Other nodes can create links leading to it.
  
**Examples:**
```python
>>> nodeA = Node(name="Node A", props={"p1": "v1", "p2": "v2"}, type="root")
[!] Created node A
>>> nodeB = Node(name="B")
[!] Created node B
>>> nodeC = Node("C")
[!] Created node C
```
### Basic node methods
##### Resetting a node
Resetting a node will wipe it's list of links, properties and, parent.
```python
>>>nodeA.reset()
```
##### Renaming a node
```python
>>>nodeA.rename("newName")
```
##### Get a node's name
```python
>>>nodeName = nodeA.name()
```
##### Get a node's type
```python
>>>nodeType = nodeA.type()
```
##### Get a node's parent
```python
>>>parentNode = nodeA.parent()
```
##### Get a node's root (parent of the parent of...of the node)
```python
>>>nodeRoot = nodeA.root()
```
##### Get a node's properties
```python
>>>nodeProps = nodeA.getProperties()
```
##### Get a node's specific property
```python
>>>nodeProps = nodeA.getProp(key="prop1")
```
##### Add a property to node 
```python
>>>nodeProps = nodeA.addProp(key="prop1", value="value1")
```
##### Drop a property from node 
```python
>>>nodeProps = nodeA.dropProp(key="prop1")
```
##### Check if a node is valid by its props
```python
>>>valid = nodeA.validateProps(pattern={
	{
    	"prop1": [["<", 10], [">", 9]]
	}
})
```
**Note** the allowed operations are: `==`, `!=`, `<=`, `>=`, `<`, `>`, and each list of elements is considered as a set of conjunction of conditions (condition1 AND condition2). 

#### Linking two nodes
```python
link(attribute, node, mode=1, power=1, generate=True)
```
Root and regular nodes can create links leading to other nodes. Each link has an attribute that defines the meaning of the link, a mode 0 or 1 being negative or positive meaning respectively, the mode is mainly used used to define the negative of the attribute, and the power(strength) of the link being an integer between 0 and 10.

**Note:** In order to avoid building the graph at each operation, SemaWal builds a static graph that is used for the search operations. Operation that define the graph like the "link" function execute a rebuild of the static graph after which can slow the execution of the code, and to prevent that is is highly recommended to set the `generate` parameter to `false` when defining a network with relatively big size.

**Node:** In case of defining a bidirectional link, it is more convenient to use the `mutualLink` method. 

**Examples:**
```python
## One-way relation: Ex: A has B
# mode (int): 0=negative, 1=positive
>>> nodeA.link(attribute="has", node=NodeB, mode=1, power=7, generate=False)
## Mutual Link: Ex: A is B and B is A
>>> nodeA.mutualLink(attribute="is", node=NodeB, mode=1, power=5)
```

**Tip:** Let's say you want to create a link between a link a node A and a list of nodes, calling the `link` method every time with the same parameters is annoying. As a solution to that SemaWal provides the `andWith()` method to create a chain of links.
```python
andWith(self, node, attribute="", mode="", power="", generate=False)
```
Of course, you can change the parameters at any point. Just be aware that the changed parameters will affect the rest of the links after the change. And don't forget to set `generate` to `True` at the last call.
**Examples:**
```python
>>>nodeA.link(attribute="has", node=NodeB, mode=1, power=7, generate=False).andWith(nodeB).andWith(nodeC, generate=True)
```
##### Generating the static graph
We mentioned earlier how to prevent the generation of the static graph. Now, generating it is simply calling the `generateStaticLinks` method, or simply `commit`.
```python
>>>nodeA.generateStaticLinks()
#or
>>>nodeA.commit()
```

#### Extending a node
When working with big networks, having nodes that share similar properties and links is very normal, and normally the developer has to define the nodes and rewrite the same properties and link for each node. In SemaWal, it is possible to define one node and then extend other nodes with it.
The nodes that extend this node get a copy of the parent node properties and links, and while the links of the child not are updated after each update of the parent links, the properties are not updated.
##### Important rules
When a node extends another, the child gets the properties of the parent node, and if they both share the same property with different values, the child node will keep its own value.
inheriting links works is simple, the child node gets the parent nodes. the inherited links are updated after each change to the parent links. If both the parent and the child have a link with the same node on the same attribute, the child's link is only updated if the power of the parent link higher than the child's link power. 
**Example:**
```python
>>> ## Inheritance (A inherits B relations): Ex: A extends B
>>> nodeA.extends(node=NodeC)
```
**WARNING!** as of version 0.2 Semawal does does not detect the circles. A circle happens when two nodes extend each other directly or indirectly. A circle can cause an infinite loop.
##### Dropping a link
```python
dropLink(attribute, node, generate=True)
```
A link can be dropped only if it is not inherited. Local links can be dropped by calling the `drop` method.
```python
>>>nodeA.dropLink("is", nodeB)
```
##### Get a list of all the links
```python
>>>nodeA.getLinks(generate=True)
```
##### Print the list of links
```python
>>>nodeA.showLinks(generate=True)
```
**Output**
```
nodeA       |  relation:  test0     |   nd_0         | mode:  1  power:  1
nodeA       |  relation:  test1     |   nd_1         | mode:  0  power:  7
```
##### Get a list of all the links attributes
```python
>>>nodeA.getLinksAttributes()
["test0", "test1"]
```
##### Get all the links (relations) with a specific node
```python
>>>nodeA.getRelationsWith(nodeB)
["test0", "test1"]
```
##### Search for for connections with filters
```python
getConnections(attributes=[], props = [], mode = -1, minPower=0, maxPower=10)
```
* **attributes**: A list of the allowed links attributes. An empty list means that all attributes are accepted.
* **props**: A dictionary of conditions exactly the same as the one to pass to the `validateProps` method. Only valid connections will be accepted.
* **mode**: 0 for only negative links, 1 for only positive links, -1 for all links.
##### Check for a series of nodes that follow a given pattern (BETA)
```python
checkPattern(pattern, ignoreList=[])
```
* **pattern**: the pattern on which the nodes shall be tested
* **ignoreList**: a list of nodes to ignore while searching
A pattern is a list of dictionaries. Its logic is exactly as a Finite-state machine, a pattern is a list of stats, each stat can have specific amount of recursive calls, if SemaWal does not find nodes that fits the next stat it exits, or else it returns a list of all the found series.
**An example pattern**
```python
[
    {
        "num":-1, # number of iterations
        "attributes": ["test1"],# Allowed attributes
        "props": {}, # Properties to validate nodes based on
        "mode": -1,
        "minPower": 0,
        "maxPower":10
    }
]
```  

**Examples**
```python
>>>nodeA.checkPattern([
    {
        "num":2,
        "attributes": ["test1"],
        "props": {},
        "mode": -1,
        "minPower": 2,
        "maxPower":4
    },
	{
        "num":1,
        "attributes": ["test0"],
        "props": {},
        "mode": -1,
        "minPower": 5,
        "maxPower":6
    },
])
```
---
### SemaWal Network object
In SemaWal a network is a special node. A node that can contain other nodes.
This definition allows SemaWal to have a more complex representations of sub-networks.
Since a network is basically a node, it has access to all the node methods, plus a set of network methods allowing for more advanced search operations.
To use the Network you have to import the Net class as the following:
```python
from semawal.net import Net
```
#### Create a network
```python
Net(name="Network", description="", props={}, type="regular")
```
**Example**
```python
>>>netA = Net()
>>>netB = Net("NetB")
>>>netC = Net(name="NetC", description="This network is to illustrate SemaWal Net")
```
All the basic methods like renaming, getting the name, Ext are exactly the same as the Node's methods.
##### Get a Network description
```python
>>>d = netA.desc()
```
##### Set a Network description
```python
>>>netA.setDesc("New description")
```
##### Append nodes & networks
```python
append(node)
# or for a list of items
appendAll(nodes)
```
**Example**
```python
>>>netA.append(nodeA)
>>>netA.append(netB)
# or for a list of items
>>>netA.appendAll([nodeC, nodeD, NetC])
```
##### Drop a node or a network
```python
drop(node)
```
**Example**
```python
>>>netA.drop(nodeA)
```
##### Get a list of all the nodes
```python
>>>netA.getNodes()
```
##### Get a node by its name
```python
>>>nodeA = net.getNode("nodeA")
```
##### Get nodes of type "root"
```python
>>>rootNodes = net.roots()
```
##### Get sub-networks
```python
>>>retNodes = net.nets()
```
##### Print all the links of all the nodes in the network
```python
>>>net.showLinks(node=None)
```
* **node**: A node from which the search begins. If it is set to None, the search starts from the root nodes. Be carful, picking a regular node might leave the root nodes out of consideration.
##### Get a list of filtered nodes
```python
fetch(props = {}, type="all") # type can be: all, root, regular, leaf
```
This method will run through all the nodes picking only those that fit the given parameters.
**Example**
```python
>>>selectedNodes = net.fetch(props = {}, type="all")
```
##### Get a list of accessible nodes from a starting node
```python
fetchFrom(node, depth=-1, type="all", allowedAttributes=[], props={}, mode=-1, minPower=0, maxPower=10, ignoreNodes=[])
```
* **node**: the start point(node).
* **depth**: the depth of the search tree. -1 means undefined depth.
  
##### Find path between two nodes
```python
findPath(nodeA, nodeB, depth=-1, allowedAttributes=[], props={}, mode=-1, minPower=0, maxPower=10, ignoreNodes=[])
```
---
### SemaWal JSON parser
SemaWal 0.2 comes with a JSON parser that can import and export both nodes and network. This mechanism allows for a more friendly use and ease the processing of sharing work.
To use the JSON parser you have to import the parser class as the following:
```python
from semawal.json_parser import Parser
```

#### Exporting a node or a network
Exporting a node or a network is as simple as calling the `export` function
```python
export(object, filename)
```
**Example**
```python
>>>Parser.export(net, "net.json")
>>>Parser.export(node, "node.json")
```
#### Importing a node or a network
In order to import a node or a network, it must be well formed and organized.
An example of a node JSON file:
```json
{
    "type": "node",//important
    "node": {
        "name": "Node1",//important
        "type": "leaf",
        "props": {
            "size": "13ko",
            "year": 1999 
        }
    }
}
```
An example of a network JSON file:
```json
{
    "name": "Network", 
    "desc": "This net is just an example of how you can use SemaWal", 
    "type": "net",
    "__comment__": "Comments like this one will not be included in the parsing process", 
    "nodes": [
        "node.json",//This will read the file node.js and create a node/network from it
        "test_node",//This will create a node with the name being "test_node"
        {"name": "1", "type": "root", "props": {"p": 1, "p2": 2}, "parent": null},//Direct node definition
        {"name": "2", "type": "regular", "props": {"s":4}, "parent": null}, 
        {"name": "3", "type": "regular", "props": {}, "parent": null}, 
        {"name": "4", "type": "regular", "props": {}, "parent": "1"}//Here node "4" will extend node "1"
    ], 
    "links": [
        {"from": "1", "to": "2", "attribute": "test", "mode": 1, "power": 1}, 
        {"from": "2", "to": "3", "attribute": "test", "mode": 1, "power": 3, "mutual": true}, 
        {"from": "3", "to": "4", "attribute": "test", "mode": 1, "power": 1}
    ]
}
```

Importing a node/network
```python
>>>net = Parser.read("net.json")
# or
>>>node = Parser.read("node.json")
```