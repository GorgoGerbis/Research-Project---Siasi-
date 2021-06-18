import os
from src import ProcessInputData
from src.NodeObj import NodeObj
from src.Request import Request
from src.PathObj import PathObj

from src.ProcessPathing import RUN_PATH_ONE
from src.ProcessPathing import RUN_PATH_TWO

# Need these for path finding and graphing
import networkx as nx
import matplotlib.pyplot as plt
from itertools import islice


"""
"Head vs Wall" Protocol or HvWProtocol
author: Jackson Walker

Head vs Wall is the nickname I gave to this protocol. Works as follows.

1) Takes in request and begins processing.
2) Gather every single possible traversable path from point a to b and turn
    them into PathObj objects.
3) Begin the process of combing through each path separating the ones 
   that meet the required criteria for success and those that don't.
4) Successful paths are then put into a list of backup paths.
5) Sort through BACKUP_PATHS and find the most optimum path.
6) Map that path to the network.
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


def remove_inadequate_paths(p, r):
    if len(p) < len(r.requestedFunctions):
        return False
    else:
        return True


if __name__ == '__main__':
    print("Begin Processing requests using: 'Head vs. Wall' Protocol\n")

    print("BEGIN PROCESSING INPUT DATA\n")
    ProcessInputData.processAllInputData()
    print("INPUT DATA PROCESSED\n")

    set_edges()
    GRAPH.add_edges_from(edges)
    # set_nodes()  # I want to maybe play around with the attributes so I might still need this Todo Need to fix set_nodes()

    # Just commented out so I don't have to keep closing the window every time
    # nx.draw(GRAPH, with_labels=True, font_weight='bold')
    # plt.show()  # ToDo Need to figure out why I need this in order to stop the graph from disappearing

    ############# SETUP IS NOW OVER WE CAN BEGIN PROCESSING ##############

    for req in Request.STATIC_TOTAL_REQUEST_LIST:   # STEP ONE
        print("BEGUN PROCESSING REQUEST: {} Source: {} Destination {} Functions: {}\n".format(req.requestID, req.source, req.destination, req.requestedFunctions))

        count = 1  # Needs to be reset to 1 when a new request is being processed
        current_request_data = [req.requestedFunctions, req.request_delay_threshold, req.requestedBW]    # Can add to this later as needed
        current_request_all_possible_paths = nx.all_simple_paths(GRAPH, req.source, req.destination)

        for path in current_request_all_possible_paths:     # STEP TWO
            if remove_inadequate_paths(path, req):  # Only paths who have enough nodes for mapping can move forward
                pathID = "R{}P{}".format(req.requestID, count)  # Ex: Given request 4 and path 20 would be: R4P20
                new_path_obj = PathObj(pathID, path, 0, current_request_data, [], 0, 0, 0)     # ToDo should make a static list of all paths being processed for a single request
                count += 1
            else:
                continue

        ############## TESTING ###############
        # RUN_PATH_ONE(PathObj.StaticPathsList, req)   # <--- Step 3, 4 and 5 starts here
        RUN_PATH_TWO(PathObj.StaticPathsList, req)

    print("ALL DONE FINDING FIRST PATHS\n")
    for op in PathObj.StaticOptimalPathsList:
        print(op+" | PATH ONE | WITHOUT FAULT TOLERANCE |\n")
    print("END\n")