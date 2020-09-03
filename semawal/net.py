#!/usr/bin/python
# -*- coding=utf-8 -*-
#TODO make it so that a node can have a relation with a network
from .node import Node

class Net(Node):
    def __init__(self, name="Network"):
        super().__init__(name=name) 
        self.__name = name
        self.__nodes = list()
        self.__roots = list()
        print("[!] Created network ", name)

    def __str__(self):
        return self.__name

    def __getattr__(self, name):
        def function():
            print("You tried to call a method named: %s" % name)
        return function

    def name(self):
        return self.__name

    def rename(self, name):
        self.__name = name
        return self

    def append(self, node):
        if node not in self.__nodes:
            self.__nodes.append(node)
            if isinstance(node, Node) and node.type() == "root":
                self.__roots.append(node)
        return self

    def appendAll(self, nodes):
        for node in nodes:
            self.append(node)

    def drop(self, node):
        if node in self.__nodes:
            self.__nodes.remove(node)

            if node in self.__roots:
                self.__roots.remove(node)
        return self

    def roots(self):
        return self.__roots

    def nodes(self):
        return self.__nodes

    def reset(self):
        self.__nodes=list()
        self.__roots=list()
        
    def showLinks(self, node=None):
        if node == None:
            for node in self.__nodes:
                node.showLinks()
        # elif isinstance(node, Node) and node in self.__nodes:
        #     toVisit = [node]
        #     visited = list()
        #     for n in toVisit:
        #         n.showLinks()
        #         for nd in n.getConnections():
        #             if nd not in visited and nd in self.__nodes:
        #                 toVisit.append(nd)
        #         visited.append(n)
        #         toVisit.remove(n)

    def fetch(self, props = {}, type="all"):
        tmp = list()
        for node in self.__nodes:
            if (type == "all" or node.type() == type) and node.validateProps(props):
                tmp.append(node)
        return tmp

    def fetchFrom(self, node, depth=-1, type="all", allowedAttributes=[], props={}, mode=-1, minPower=0, maxPower=10, ignoreNodes=[]):
        tmp=[node]
        connections = node.getConnections(attributes=allowedAttributes, props=props, mode=mode, minPower=minPower, maxPower=maxPower)
        ignoreNodes.append(node)

        if depth != 0:
            for n in connections:
                if n in self.__nodes and n not in ignoreNodes:
                    tmp = tmp + self.fetchFrom(n, depth=(depth-1), type=type, allowedAttributes=allowedAttributes, props=props, mode=mode, minPower=minPower, maxPower=maxPower, ignoreNodes=ignoreNodes)
        return tmp

    #, ignoredAttributes=[]
    def findPath(self, nodeA, nodeB, depth=-1, allowedAttributes=[], props={}, mode=-1, minPower=0, maxPower=10, ignoreNodes=[]):
        connections = nodeA.getConnections(attributes=allowedAttributes, props=props, mode=mode, minPower=minPower, maxPower=maxPower)
        ignoreNodes.append(nodeA)
        if connections == [] or depth == 0:
            return []

        elif nodeB in connections and nodeB:
            return [nodeA, nodeB]

        else:
            for node in connections:
                if node in self.__nodes and node not in ignoreNodes:
                    path = self.findPath(nodeA=node,nodeB=nodeB, depth=(depth-1), allowedAttributes=allowedAttributes, props=props, mode=mode, minPower=minPower, maxPower=maxPower, ignoreNodes=ignoreNodes)
                    if path != None and len(path) != 0:
                        return [nodeA] + path
        return []

# isinstance(props, dict)

    # def getNodeskeys(self):
    #     l = list()
    #     for n in self.nodes.values():
    #         if type(n) is Node:
    #             l.append(n.__name)
    #     return l

    # def add(self, *nodes):
    #     for n in nodes:
    #         self.nodes[n.__name] = n

    # def getNode(self, nodeName):
    #     return self.nodes[nodeName]

    # def search(self, node, depth=2, visited_nodes = []):
    #     if type(node) is str:
    #         node = self.getNode(node)
    #     node.showLinks()
    #     visited_nodes.append(node)
    #     items = self.nodes.values()
    #     if depth > 0:
    #         for elem in node.connections():
    #             if type(node) is Net:
    #                 continue
    #             if elem in items and elem not in visited_nodes:
    #                 visited_nodes = self.search(elem, depth=(depth-1), visited_nodes=visited_nodes)
    #     return visited_nodes

    # def randomSearch(self, returnstr = False):
    #     visited_nodes = []
    #     items = self.nodes.values()
    #     for node in items:
    #         if type(node) is Net:
    #             continue
    #         if node in items and node not in visited_nodes:
    #             visited_nodes = self.search(node, depth=0, visited_nodes=visited_nodes)
    
    # def filter(self, alist):
    #     r = list()
    #     items = self.nodes.values()
    #     for elem in alist:
    #         if elem in items:
    #             r.append(elem)
    #     return r
        
    # def __connected(self, a, b):
    #     for elem in a:
    #         for elemB in b:
    #             if elem == elemB:
    #                 return [elem]
    #     return []

    # def areConnected(self, nodeA, nodeB, nlist = [], ignore = [], checked = [], all_connections=True):
    #     items = self.nodes.values()
    #     if nodeA not in items or nodeB not in items:
    #         return []
    #     if nodeA == nodeB:
    #         return [nodeA]

    #     checked.append(nodeA)

    #     nlist = self.filter(list(nodeA.connections(all=all_connections)))
        
    #     for elem in nlist:
    #         if elem in checked:
    #             continue
    #         if nodeB in elem.connections(all=all_connections):
    #             return [nodeA, elem, nodeB]
    #         r = self.areConnected(elem, nodeB, all_connections=all_connections)
    #         if r != []:
    #             return [nodeA] + r
    #     return []

    # def isLinkedBy(self, nodeA, link, nodeB, all_connection = True):
    #     path = self.areConnected(nodeA=nodeA, nodeB=nodeB, checked=[], nlist=[], all_connections=all_connection)
    #     if path == []:
    #         return False
        
    #     for i in range(len(path)-1):
    #         if ( link not in path[i].relationsWith(path[i+1])):
    #             return False
    #     return True

    # def drawPath(self, nodeA, nodeB, all_connections = True):
    #     path = self.areConnected(nodeA=nodeA, nodeB=nodeB, checked=[], nlist=[], all_connections=all_connections)
    #     if path == []:
    #         print("No path has been found between ", nodeA.__name, " and ", nodeB.__name)
    #         return
        
    #     print("Printing the path:")
    #     for i in range(len(path)-1):
    #         print(path[i].__name, "\t|  ", path[i].relationsWith(path[i+1]), "\t|  ", path[i+1].__name)
