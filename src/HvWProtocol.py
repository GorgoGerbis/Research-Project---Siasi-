import os
from src import ProcessInputData
from src.NodeObj import NodeObj
from src.Request import Request
from src.PathObj import PathObj
import CreateOutputData
from src.CreateOutputData import output_file_PATH_TWO
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

REQUEST_DELAY_THRESHOLD = 120.5

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


def process_path_one():
    for req in Request.STATIC_TOTAL_REQUEST_LIST:   # STEP ONE
        print("BEGUN PROCESSING REQUEST: {} Source: {} Destination {} Functions: {}\n".format(req.requestID, req.source, req.destination, req.requestedFunctions))

        count = 1  # Needs to be reset to 1 when a new request is being processed
        current_request_data = [req.requestedFunctions, req.request_delay_threshold, req.requestedBW]
        current_request_all_possible_paths = nx.all_simple_paths(GRAPH, req.source, req.destination)

        for path in current_request_all_possible_paths:     # STEP TWO
            if len(path) != 0:
                pathID = "R{}P{}".format(req.requestID, count)
                # ToDo should make a static list of all paths being processed for a single request
                new_path_obj = PathObj(pathID, path, 0, current_request_data, [], 0, 0, 0, 2)

                ProcessPathing.set_path_state_PATH_ONE(new_path_obj)

                count += 1

        RUN_PATH_ONE(req)   # <--- Step 3, 4 and 5 starts here


def process_path_two():
    for req in Request.STATIC_TOTAL_REQUEST_LIST:   # STEP ONE
        print("BEGUN PROCESSING REQUEST: {} Source: {} Destination {} Functions: {}\n".format(req.requestID, req.source, req.destination, req.requestedFunctions))

        count = 1  # Needs to be reset to 1 when a new request is being processed
        current_request_data = [req.requestedFunctions, req.request_delay_threshold, req.requestedBW]
        current_request_all_possible_paths = nx.all_simple_paths(GRAPH, req.source, req.destination)

        for path in current_request_all_possible_paths:     # STEP TWO
            if len(path) != 0:
                pathID = "R{}P{}".format(req.requestID, count)
                # ToDo should make a static list of all paths being processed for a single request
                new_path_obj = PathObj(pathID, path, 0, current_request_data, [], 0, 0, 0, 2)

                ProcessPathing.set_path_state_PATH_TWO(new_path_obj)

                count += 1

        RUN_PATH_TWO(req)


def reset_all_resources():
    for node in NodeObj.StaticNodeList:
        node.reset_node()
        print("RESET NODE {}".format(node.nodeID))

    for link in NodeObj.StaticLinkList:
        link.reset_link()
        print("RESET LINK {}".format(link.linkID))


def create_figure_ONE():
    plt.title("FIGURE 1: Number of incoming requests vs. Average delay per request")
    plt.xlabel("Number of incoming requests")
    plt.ylabel("Average delay per request")

    max_delay = 80

    average_list_PO = []
    average_list_PT = []
    count = 0
    cnt = 0
    current_average_PO = 0
    current_average_PT = 0

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_ONE
        if obj is not None:
            add = 0
            current_average_PO = obj.DELAY
            for i in average_list_PO:
                add += i
            count += 1
            current_average_PO = (current_average_PO + add) / count
            average_list_PO.append(current_average_PO)

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_TWO
        if obj is not None:
            add = 0
            current_average_PT = obj.DELAY
            for i in average_list_PT:
                add += i
            cnt += 1
            current_average_PT = (current_average_PT + add) / cnt
            average_list_PT.append(current_average_PT)

    plt.axis([1, len(average_list_PO), 1, max_delay])
    plt.plot(average_list_PO)
    plt.plot(average_list_PT, color='r')
    plt.show()


def create_figure_TWO():
    plt.title("FIGURE 2: Number of incoming requests vs. Average cost per request")
    plt.xlabel("Number of incoming requests")
    plt.ylabel("Average cost per request")

    max_cost = 80

    average_list_PO = []
    average_list_PT = []
    count = 0
    cnt = 0
    current_average_PO = 0
    current_average_PT = 0

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_ONE
        if obj is not None:
            count += 1
            add = 0
            current_average_PO = obj.COST
            for i in average_list_PO:
                add += i
            current_average_PO = (current_average_PO + add) / count
            average_list_PO.append(current_average_PO)

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_TWO
        if obj is not None:
            cnt += 1
            add = 0
            current_average_PT = obj.COST
            for i in average_list_PT:
                add += i
            current_average_PT = (current_average_PT + add) / cnt
            average_list_PT.append(current_average_PT)

    plt.axis([1, len(average_list_PO), 1, max_cost])
    plt.plot(average_list_PO)
    plt.plot(average_list_PT, color='r')
    plt.show()


def create_figure_THREE():
    plt.title("FIGURE 3: Number of incoming requests vs. Number of failed requests")
    plt.xlabel("Number of incoming requests")
    plt.ylabel("Number of failed requests")

    num_passed = 0
    num_failed = 0

    num_passed_other = 0
    num_failed_other = 0

    x_list = []
    y_list = []

    a_list = []
    b_list = []

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        if req.requestStatus[0] == 3:
            num_passed += 1
            y_list.append(num_failed)
        elif req.requestStatus[0] == 2:
            num_failed += 1
            y_list.append(num_failed)

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        if req.requestStatus[1] == 3:
            num_passed_other += 1
            b_list.append(num_failed_other)
        elif req.requestStatus[1] == 2:
            num_failed_other += 1
            b_list.append(num_failed_other)

    plt.axis([0, len(y_list), 0, num_failed_other])
    plt.plot(y_list)
    plt.plot(b_list, color='r')
    plt.show()


def find_isolated_nodes():
    frick = []
    frack = []

    output = []

    for n in NodeObj.StaticNodeList:
        frick.append(n.nodeID)

    for n in GRAPH:
        frack.append(n)

    for n in frick:
        if n not in frack:
            output.append(n)

    print("The following nodes are not accessible: {}\n".format(output))

if __name__ == '__main__':
    print("Begin Processing requests using: 'Head vs. Wall' Protocol\n")
    print("BEGIN PROCESSING INPUT DATA\n")
    ProcessInputData.processAllInputData()
    print("INPUT DATA PROCESSED\n")

    set_edges()
    GRAPH.add_edges_from(edges)

    # Just commented out so I don't have to keep closing the window every time
    nx.draw(GRAPH, with_labels=True, font_weight='bold')
    plt.show()  # ToDo Need to figure out why I need this in order to stop the graph from disappearing

    find_isolated_nodes()

    ############# SETUP IS NOW OVER WE CAN BEGIN PROCESSING ##############
    process_path_one()
    print("ALL DONE FINDING FIRST PATHS\n")
    for op in PathObj.StaticOptimalPathsList:
        print(op)

    print("STARTING CREATION OF OUTPUT FILES\n")
    CreateOutputData.output_file_PATH_ONE()
    print("CREATED PATH ONE OUTPUT FILES\n")
    ##########################################################

    print("RESETTING NODE AND LINK RESOURCES\n")
    reset_all_resources()

    ############# BEGIN PROCESSING FOR PATH TWO ##############
    process_path_two()
    print("ALL DONE FINDING SECOND PATHS\n")
    for op in PathObj.StaticOptimalPathsList:
        print(op)

    print("STARTING CREATION OF FAILURE PROBABILITY OUTPUT FILES\n")
    output_file_PATH_TWO()
    ##########################################################

    ############# CREATE OUTPUT DATA GRAPHS ##############
    create_figure_ONE()
    create_figure_TWO()
    create_figure_THREE()
