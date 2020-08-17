#TODO make it so that a node can have a relation with a network
from node import Node

class Net(object):
    value = ""
    nodes = []
    def __init__(self, name="Network"):
        self.nodes = dict()
        self.value = name
        print("[!] Created network ", name)

    def __str__(self):
        return self.value

    def __getattr__(self, name):
        def function():
            print("You tried to call a method named: %s" % name)
        return function

    def getNodeskeys(self):
        l = list()
        for n in self.nodes.values():
            if type(n) is Node:
                l.append(n.value)
        return l

    def add(self, *nodes):
        for n in nodes:
            self.nodes[n.value] = n

    def getNode(self, nodeName):
        return self.nodes[nodeName]

    def search(self, node, depth=2, visited_nodes = []):
        if type(node) is str:
            node = self.getNode(node)
        node.showLinks()
        visited_nodes.append(node)
        items = self.nodes.values()
        if depth > 0:
            for elem in node.connections():
                if type(node) is Net:
                    continue
                if elem in items and elem not in visited_nodes:
                    visited_nodes = self.search(elem, depth=(depth-1), visited_nodes=visited_nodes)
        return visited_nodes

    def randomSearch(self, returnstr = False):
        visited_nodes = []
        items = self.nodes.values()
        for node in items:
            if type(node) is Net:
                continue
            if node in items and node not in visited_nodes:
                visited_nodes = self.search(node, depth=0, visited_nodes=visited_nodes)
    
    def filter(self, alist):
        r = list()
        items = self.nodes.values()
        for elem in alist:
            if elem in items:
                r.append(elem)
        return r
        

    def __connected(self, a, b):
        for elem in a:
            for elemB in b:
                if elem == elemB:
                    return [elem]
        return []

    def areConnected(self, nodeA, nodeB, nlist = [], ignore = [], checked = [], all_connections=True):
        items = self.nodes.values()
        if nodeA not in items or nodeB not in items:
            return []
        if nodeA == nodeB:
            return [nodeA]

        checked.append(nodeA)

        nlist = self.filter(list(nodeA.connections(all=all_connections)))
        
        for elem in nlist:
            if elem in checked:
                continue
            if nodeB in elem.connections(all=all_connections):
                return [nodeA, elem, nodeB]
            r = self.areConnected(elem, nodeB, all_connections=all_connections)
            if r != []:
                return [nodeA] + r
        return []

    def isLinkedBy(self, nodeA, link, nodeB, all_connection = True):
        path = self.areConnected(nodeA=nodeA, nodeB=nodeB, checked=[], nlist=[], all_connections=all_connection)
        if path == []:
            return False
        
        for i in range(len(path)-1):
            if ( link not in path[i].relationsWith(path[i+1])):
                return False
        return True


    def drawPath(self, nodeA, nodeB, all_connections = True):
        path = self.areConnected(nodeA=nodeA, nodeB=nodeB, checked=[], nlist=[], all_connections=all_connections)
        if path == []:
            print("No path has been found between ", nodeA.value, " and ", nodeB.value)
            return
        
        print("Printing the path:")
        for i in range(len(path)-1):
            print(path[i].value, "\t|  ", path[i].relationsWith(path[i+1]), "\t|  ", path[i+1].value)