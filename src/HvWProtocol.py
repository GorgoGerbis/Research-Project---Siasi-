import os
from src.NodeObj import NodeObj
from src.Request import Request
from src import processInputData

# Need these for path finding
import networkx as nx
import matplotlib.pyplot as plt
from itertools import islice

"""
"Head vs Wall" Protocol or HvWProtocol
author: Jackson Walker

Head vs Wall is the nickname I gave to this protocol. Works as follows.

1) Takes in request and begins processing.
2) Gather every single possible traversable path from point a to b.
3) Begin the process of combing through each path separating the ones 
   that meet the required criteria for success and those that don't.
4) Successful paths are then put into a list where they are then
   turned into 'PathObj' objects.
5) Sort these 'PathObj' objects and find the most optimum path.
"""

# Variables to set up graph for network
GRAPH = nx.Graph()
edges = []

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
        if current_node_id not in visited_nodes:
            GRAPH.add_node(current_node_id)
            visited_nodes.append(current_node_id)


if __name__ == '__main__':
    print("Begin Processing requests using: 'Head vs. Wall' Protocol\n")

    print("BEGIN PROCESSING INPUT DATA\n")
    processInputData.processAllInputData()
    print("INPUT DATA PROCESSED\n")

    print("CREATING GRAPH\n")
    # set_nodes()   # I want to maybe play around with the attributes so I might still need this
    set_edges()
    GRAPH.add_edges_from(edges)
    print("GRAPH CREATED\n")

    nx.draw(GRAPH, with_labels=True, font_weight='bold')
    plt.show()  # Need to figure out why I need this in order to stop the graph from disappearing

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        print("BEGUN PROCESSING REQUEST: {}\n".format(req.requestID))
        current_request_all_possible_paths = nx.all_simple_paths(GRAPH, req.source, req.destination)
        # for path in current_request_all_possible_paths:
        #     print(path)
