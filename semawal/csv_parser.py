#!/usr/bin/python
# -*- coding=utf-8 -*-
from .node import Node
from .net import Net
import csv
import os
import re

class parser(object):
    
    @staticmethod
    def read(filename):
        if not filename.endswith('.csv'):
            return False
        if not os.path.isfile(filename):
            return False
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            nodes = dict()
            nodeList = list()
            csv_content = list()

            for row in csv_reader:
                print(row)
                csv_content.append(row)
                nodeList.append(row[0])
                nodeList.append(row[2])
            
            nodeList = set(nodeList)
            for elem in nodeList:
                if elem.endswith('.csv'):
                    nodes[elem] = parser.read(elem)
                else:
                    nodes[elem] = Node(elem)

            for row in csv_content:
                if row[1] == "extends":
                    nodes[row[0]].extends(nodes[row[2]])
                else:
                    nodes[row[0]].link(row[1], nodes[row[2]], row[3], row[4])

        n = Net(filename[:-4])

        for node in nodes.items():
            n.add(node[1])
        return n
