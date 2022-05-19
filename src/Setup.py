"""
Setup Script
author: Jackson Walker

Responsible for setup simulation including all parameters and network graphs.
1. Needs to setup network graph.
2. Needs to initialize all necessary objects.
3. ???
"""
# Need these for path finding and graphing
import networkx as nx
import matplotlib.pyplot as plt

from src.NodeObj import NodeObj
from src.Request import Request
from src.PathObj import PathObj

#@ToDo NEED A LIVE STATUS AND UPDATE OF CURRENT REQUEST BEING PROCESSED
#@ToDo Need to implement old functions from main

# Variables to set up graph for network
GRAPH = nx.Graph()
edges = []
nodes = []


def set_edges():
    visited_links = []

    for link in NodeObj.StaticLinkList:
        u = link.linkSrc
        v = link.linkDest
        temp = [u, v]
        if link not in visited_links:
            edges.append(temp)
            visited_links.append(link)


def set_nodes():
    visited_nodes = []

    for node in NodeObj.StaticNodeList:
        current_node_id = int(node.nodeID)
        if node not in visited_nodes:
            nodes.append(node)
            visited_nodes.append(current_node_id)


def setup():
    set_edges()
    GRAPH.add_edges_from(edges)

    # Just commented out so I don't have to keep closing the window every time
    nx.draw(GRAPH, with_labels=True, font_weight='bold')
    plt.show()