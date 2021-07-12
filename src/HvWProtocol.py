from src import ProcessInputData
from src.NodeObj import NodeObj
from src.Request import Request
from src.PathObj import PathObj
from src.CreateOutputData import output_file_PATH_ONE
from src.CreateOutputData import output_file_PATH_TWO
from src.CreateOutputData import create_data_graph
import ProcessPathing

# Need these for path finding and graphing
import networkx as nx
import matplotlib.pyplot as plt
from itertools import islice

# Need these to process requests
from src.ProcessPathing import RUN_PATH_ONE
from src.ProcessPathing import RUN_PATH_TWO

# Creating output files
import src.CreateOutputData

REQUEST_DELAY_THRESHOLD = 30.5

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

The networkx method 'all_simple_paths' uses a modified depth first search.
"""

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


if __name__ == '__main__':
    print("Begin Processing requests using: 'Head vs. Wall' Protocol\n")

    print("BEGIN PROCESSING INPUT DATA\n")
    ProcessInputData.processAllInputData()
    print("INPUT DATA PROCESSED\n")

    set_edges()
    GRAPH.add_edges_from(edges)
    # set_nodes()  # I want to maybe play around with the attributes so I might still need this Todo Need to fix set_nodes()
    # GRAPH.add_nodes_from(nodes)

    # Just commented out so I don't have to keep closing the window every time
    nx.draw(GRAPH, with_labels=True, font_weight='bold')
    plt.show()  # ToDo Need to figure out why I need this in order to stop the graph from disappearing

    ############# SETUP IS NOW OVER WE CAN BEGIN PROCESSING ##############

    for req in Request.STATIC_TOTAL_REQUEST_LIST:   # STEP ONE
        print("BEGUN PROCESSING REQUEST: {} Source: {} Destination {} Functions: {}\n".format(req.requestID, req.source, req.destination, req.requestedFunctions))

        count = 1  # Needs to be reset to 1 when a new request is being processed
        current_request_data = [req.requestedFunctions, req.request_delay_threshold, req.requestedBW]
        current_request_all_possible_paths = nx.all_simple_paths(GRAPH, req.source, req.destination)

        for path in current_request_all_possible_paths:     # STEP TWO
            if path != "":
                pathID = "R{}P{}".format(req.requestID, count)
                new_path_obj = PathObj(pathID, path, 0, current_request_data, [], 0, 0, 0, 2)  # ToDo should make a static list of all paths being processed for a single request

                ProcessPathing.set_path_state_PATH_ONE(new_path_obj)
                # ProcessPathing.set_path_state_PATH_TWO(new_path_obj)

                count += 1

        ############## TESTING ###############
        RUN_PATH_ONE(req)   # <--- Step 3, 4 and 5 starts here
        # RUN_PATH_TWO(req)

    x = Request.STATIC_TOTAL_REQUEST_LIST

    print("ALL DONE FINDING FIRST PATHS\n")
    for op in PathObj.StaticOptimalPathsList:
        print(op)

    print("STARTING CREATION OF OUTPUT FILES\n")
    output_file_PATH_ONE()
    # output_file_PATH_TWO()
    print("CREATED OUTPUT FILES\n")
    create_data_graph()