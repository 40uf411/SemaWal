#!/usr/bin/python
# -*- coding=utf-8 -*-
import json
from .node import Node
from .net import Net
import os
import re

class Parser:
    
    @staticmethod
    def read(filename):
        def generate_node(node):
                nd = node
                ndk= nd.keys()
                name = nd["name"]
                type = nd["type"] if "type" in ndk else None
                props = nd["props"] if "props" in ndk else {}
                return Node(name=name, type=type, props=props)
        #######################################################
        with open(filename) as json_file:
            data = json.load(json_file)
            if data["type"] == "node":
                return generate_node(data["node"])
            
            elif data["type"] == "net":
                name = data["name"]
                desc = data["desc"] if "desc" in data.keys() else ""
                nodes_ref = data["nodes"]
                links = data["links"]
                nodes = dict()
                # creating the nodes
                for nref in nodes_ref:
                    if isinstance(nref, str):
                        if nref[-5:] == ".json":
                            n = Parser.read(nref)
                            nodes[n.name()] = n
                        else:
                            nodes[nref] = Node(name=nref)
                    else:
                        nodes[nref["name"]] = generate_node(nref)
                # building the extend relation
                for nref in nodes_ref:
                    if "parent" in nref and nref["parent"] in nodes.keys():
                        nodes[nref["name"]].extends(nodes[nref["parent"]])
                # building the links
                for link in links:
                    n_from = nodes[link["from"]]
                    n_to = nodes[link["to"]]
                    attr = link["attribute"]
                    mode = link["mode"] if "mode" in link.keys() else 1
                    power = link["power"] if "power" in link.keys() else 1
                    if "mutual" in link and link["mutual"]:
                        n_from.mutualLink(attribute=attr, node=n_to, mode=mode, power=power)
                    else:
                        n_from.link(attribute=attr, node=n_to, mode=mode, power=power)
                # creating the network and inserting the nodes
                net = Net(name=name, description=desc)
                net.appendAll(nodes=nodes.values())
                return net
    
    @staticmethod
    def export(object, filename):
        #####################################################
        def transform_node(node):
            return {
                "name": node.name(),
                "type": node.type(),
                "props": node.getProperties(),
                "parent": node.parent()
            }
        #
        def transfor_link(node, attr, link):
            return {
                "from": node.name(),
                "to": link[0].name(),
                "attribute": attr,
                "mode": link[1],
                "power": link[2]
            }
        
        #####################################################
        data = dict()
        if isinstance(object, Net):
            nodes_in_net = []
            links_in_net = []
            for node in object.nodes():
                # add node to the list of nodes
                nodes_in_net.append(transform_node(node))
                
                # add node links
                nodeLinks = node.getLinks()
                for attr in nodeLinks.keys():
                    for link in nodeLinks[attr]:
                        links_in_net.append(transfor_link(node, attr, link))
            data = {
                "name": object.name(),
                "desc": object.desc(),
                "type": "net",
                "nodes": nodes_in_net,
                "links": links_in_net
            }
            
        elif isinstance(object, Node):
            data = {
                "type": "node",
                "node": transform_node(object)
            }
            
        else:
            print('[*] ERROR! not supported input type, input must be a Net or a Node.')
            
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)