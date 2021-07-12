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

# Resources
baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"

resourcesFolder = os.path.join(baseFolder, "resources")
NodeInputData = os.path.join(resourcesFolder, "NodeInputData-EXSMALL-TEST-6-24-21.csv")
LinkInputData = os.path.join(resourcesFolder, "LinkInputData-EXSMALL-TEST-6-24-21.csv")
auto_requests_Opt = os.path.join(resourcesFolder, "requests-EXSMALL-TEST-6-24-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-TEST-A-7-03-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-TEST-A-7-03-21.csv")
# auto_requests_Opt = os.path.join(resourcesFolder, "requests-TEST-A-7-03-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-TEST-B-7-03-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-TEST-B-7-03-21.csv")
# auto_requests_Opt = os.path.join(resourcesFolder, "requests-TEST-B-7-03-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-TEST-C-7-03-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-TEST-C-7-03-21.csv")
# auto_requests_Opt = os.path.join(resourcesFolder, "requests-TEST-C-7-03-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-TEST-D-7-03-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-TEST-D-7-03-21.csv")
# auto_requests_Opt = os.path.join(resourcesFolder, "requests-TEST-D-7-03-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-TEST-E-7-03-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-TEST-E-7-03-21.csv")
# auto_requests_Opt = os.path.join(resourcesFolder, "requests-TEST-E-7-03-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-TEST-F-7-03-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-TEST-F-7-03-21.csv")
# auto_requests_Opt = os.path.join(resourcesFolder, "requests-TEST-F-7-03-21.txt")

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

    max_delay = 0

    a_list = []
    b_list = []

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_ONE
        if obj is not None:
            a_list.append(obj.DELAY)

            if obj.DELAY > max_delay:
                max_delay = obj.DELAY

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_TWO
        if obj is not None:
            b_list.append(obj.DELAY)

            if obj.DELAY > max_delay:
                max_delay = obj.DELAY

    num_reqs = len(Request.STATIC_TOTAL_REQUEST_LIST)
    plt.axis([0, num_reqs, 0, max_delay+10])
    plt.plot(a_list)
    plt.plot(b_list, color='r')
    plt.show()


def create_figure_TWO():
    plt.title("FIGURE 2: Number of incoming requests vs. Average cost per request")
    plt.xlabel("Number of incoming requests")
    plt.ylabel("Average cost per request")

    max_cost = 0

    a_list = []
    b_list = []

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_ONE
        if obj is not None:
            a_list.append(obj.COST)

            if obj.COST > max_cost:
                max_cost = obj.COST

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_TWO
        if obj is not None:
            b_list.append(obj.COST)

            if obj.COST > max_cost:
                max_cost = obj.COST

    num_reqs = len(Request.STATIC_TOTAL_REQUEST_LIST)
    plt.axis([0, num_reqs, 0, max_cost])
    plt.plot(a_list)
    plt.plot(b_list, color='r')
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
            x_list.append(num_passed)
            y_list.append(num_failed)
        elif req.requestStatus[0] == 2:
            num_failed += 1
            x_list.append(num_passed)
            y_list.append(num_failed)

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        if req.requestStatus[1] == 3:
            num_passed_other += 1
            a_list.append(num_passed_other)
            b_list.append(num_failed_other)
        elif req.requestStatus[1] == 2:
            num_failed_other += 1
            a_list.append(num_passed_other)
            b_list.append(num_failed_other)

    if (num_passed + num_failed) > (num_passed_other + num_failed_other):
        num_reqs = num_passed + num_failed
    else:
        num_reqs = num_passed_other + num_failed_other

    plt.axis([0, num_reqs, -1, num_failed])
    plt.plot(x_list, y_list)
    plt.plot(a_list, b_list, color='r')
    plt.show()


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
