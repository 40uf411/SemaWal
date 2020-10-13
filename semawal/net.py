#!/usr/bin/python
# -*- coding=utf-8 -*-
from .node import Node

class Net(Node):
    ### the network is a node as well
    def __init__(self, name="Network", description="", props={}, type="regular"):
        super().__init__(name=name,props=props, type=type) 
        self.__name = name
        self.__desc = description
        self.__index = dict()
        self.__nodes = list()
        self.__roots = list()
        self.__nets  = list()
        print("[!] Created network ", name)

    def desc(self):
        return self.__desc

    def setDesc(self, description):
        self.__desc=description
        
    def append(self, node):
        if node not in self.__nodes:
            self.__nodes.append(node)
            self.__index[node.name()] = node
            if isinstance(node, Node) and node.type() == "root":
                self.__roots.append(node)
            if isinstance(node, Net):
                self.__nets.append(node)
        return self

    def appendAll(self, nodes):
        for node in nodes:
            self.append(node)

    def drop(self, node):
        if node in self.__nodes:
            self.__nodes.remove(node)
            del self.__index[node.name()]
            if node in self.__roots:
                self.__roots.remove(node)
            if node in self.__nets:
                self.__nets.remove(node)
        return self

    def roots(self):
        return self.__roots

    def nodes(self):
        return self.__nodes

    def getNode(self, nodeName):
        return self.__index[nodeName]
    
    def nets(self):
        return self.__nets
    
    def reset(self):
        self.__nodes=list()
        self.__roots=list()
        self.__index=dict()
        self.__nets=list()
        
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