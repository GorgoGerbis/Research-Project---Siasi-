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
import CONSTANTS
from src import ProcessInputData
from src.NodeObj import NodeObj
from src.RequestObj import RequestObj
from src.PathObj import PathObj
from src.OutputGraphs import run_output_graphs
import CreateOutputData

from src.CONSTANTS import GLOBAL_REQUEST_DELAY_THRESHOLD
from src.CONSTANTS import GLOBAL_SINGLE_OUTPUT_FILE_PATH_ONE
from src.CONSTANTS import GLOBAL_SINGLE_OUTPUT_FILE_PATH_TWO
from src.CONSTANTS import GLOBAL_MULTI_OUTPUT_FILE_PATH_ONE
from src.CONSTANTS import GLOBAL_MULTI_OUTPUT_FILE_PATH_TWO

from src.CONSTANTS import CREATE_NUM_NODES
from src.CONSTANTS import CREATE_NUM_LINKS
from src.CONSTANTS import CREATE_NUM_REQUESTS

# Need these for path finding and graphing
import networkx as nx
import matplotlib.pyplot as plt

# Need these to process requests
from src.MultiMapping import RUN_PATH_ONE
from src.MultiMapping import RUN_PATH_TWO
from src.SingleMapping import RUN_PATH_ONE_SINGLE_MAPPING
from src.SingleMapping import RUN_PATH_TWO_SINGLE_MAPPING


REQUEST_DELAY_THRESHOLD = GLOBAL_REQUEST_DELAY_THRESHOLD

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


def process_path_one_MULTI_MAPPING():
    for req in RequestObj.STATIC_TOTAL_REQUEST_LIST:   # STEP ONE
        print("BEGUN PROCESSING REQUEST: {} Source: {} Destination {} Functions: {}\n".format(req.requestID, req.source, req.destination, req.requestedFunctions))

        count = 1  # Needs to be reset to 1 when a new request is being processed
        current_request_data = [req.requestedFunctions, req.request_delay_threshold, req.requestedBW]
        current_request_all_possible_paths = nx.all_simple_paths(GRAPH, req.source, req.destination)

        for path in current_request_all_possible_paths:     # STEP TWO
            pathID = "R{}P{}".format(req.requestID, count)
            # ToDo should make a static list of all paths being processed for a single request
            PathObj(pathID, path, 0, current_request_data, [], 0, 0, 0, 1)
            count += 1

        RUN_PATH_ONE(req)   # <--- Step 3, 4 and 5 starts here


def process_path_two_MULTI_MAPPING():
    for req in RequestObj.STATIC_TOTAL_REQUEST_LIST:   # STEP ONE
        print("BEGUN PROCESSING REQUEST: {} Source: {} Destination {} Functions: {}\n".format(req.requestID, req.source, req.destination, req.requestedFunctions))
        s = req.source
        d = req.destination

        count = 1  # Needs to be reset to 1 when a new request is being processed
        current_request_data = [req.requestedFunctions, req.request_delay_threshold, req.requestedBW]
        current_request_all_possible_paths = nx.all_simple_paths(GRAPH, req.source, req.destination)

        for path in current_request_all_possible_paths:     # STEP TWO
            pathID = "R{}P{}".format(req.requestID, count)
            # ToDo should make a static list of all paths being processed for a single request
            PathObj(pathID, path, 0, current_request_data, [], 0, 0, 0, 2)
            count += 1

        RUN_PATH_TWO(req)


def process_path_one_SINGLE_MAPPING():
    for req in RequestObj.STATIC_TOTAL_REQUEST_LIST:   # STEP ONE
        print("BEGUN PROCESSING REQUEST: {} Source: {} Destination {} Functions: {}\n".format(req.requestID, req.source, req.destination, req.requestedFunctions))

        count = 1  # Needs to be reset to 1 when a new request is being processed
        current_request_data = [req.requestedFunctions, req.request_delay_threshold, req.requestedBW]
        current_request_all_possible_paths = nx.all_simple_paths(GRAPH, req.source, req.destination)

        for path in current_request_all_possible_paths:     # STEP TWO
            pathID = "R{}P{}".format(req.requestID, count)
            # ToDo should make a static list of all paths being processed for a single request
            PathObj(pathID, path, 0, current_request_data, [], 0, 0, 0, 1)
            count += 1

        RUN_PATH_ONE_SINGLE_MAPPING(req)   # <--- Step 3, 4 and 5 starts here


def process_path_two_SINGLE_MAPPING():
    for req in RequestObj.STATIC_TOTAL_REQUEST_LIST:   # STEP ONE
        print("BEGUN PROCESSING REQUEST: {} Source: {} Destination {} Functions: {}\n".format(req.requestID, req.source, req.destination, req.requestedFunctions))
        s = req.source
        d = req.destination

        count = 1  # Needs to be reset to 1 when a new request is being processed
        current_request_data = [req.requestedFunctions, req.request_delay_threshold, req.requestedBW]
        current_request_all_possible_paths = nx.all_simple_paths(GRAPH, req.source, req.destination)

        for path in current_request_all_possible_paths:     # STEP TWO
            pathID = "R{}P{}".format(req.requestID, count)
            # ToDo should make a static list of all paths being processed for a single request
            PathObj(pathID, path, 0, current_request_data, [], 0, 0, 0, 2)
            count += 1

        RUN_PATH_TWO_SINGLE_MAPPING(req)


if __name__ == '__main__':
    print("BEGIN PROCESSING INPUT DATA\n")
    ProcessInputData.processAllInputData()
    print("INPUT DATA PROCESSED\n")

    set_edges()
    GRAPH.add_edges_from(edges)

    # nx.draw(GRAPH, with_labels=True, font_weight='bold')
    # plt.show()

    find_isolated_nodes()

    if CONSTANTS.GLOBAL_PROTOCOL == 1:
        print("Begin Processing requests using: Single-Mapping Protocol\n")
        process_path_one_SINGLE_MAPPING()

        print("STARTING CREATION OF OUTPUT FILES\n")
        CreateOutputData.output_file_PATH_ONE(GLOBAL_SINGLE_OUTPUT_FILE_PATH_ONE, CREATE_NUM_REQUESTS, CREATE_NUM_NODES, CREATE_NUM_LINKS)
        print("CREATED PATH ONE OUTPUT FILES\n")

    if CONSTANTS.GLOBAL_PROTOCOL == 2:
        print("Begin Processing requests using: Single-Mapping Protocol\n")
        process_path_two_SINGLE_MAPPING()

        print("STARTING CREATION OF OUTPUT FILES\n")
        CreateOutputData.output_file_PATH_TWO(GLOBAL_SINGLE_OUTPUT_FILE_PATH_TWO, CREATE_NUM_REQUESTS, CREATE_NUM_NODES,
                                              CREATE_NUM_LINKS)
        print("CREATED PATH ONE OUTPUT FILES\n")

        # for link in NodeObj.StaticLinkList:
        #     del link
        # NodeObj.StaticLinkList.clear()
        #
        # for node in NodeObj.StaticNodeList:
        #     del node
        # NodeObj.StaticNodeList.clear()
        #
        # ProcessInputData.processInputDataNode(ProcessInputData.NodeInputData)
        # ProcessInputData.processInputDataLink(ProcessInputData.LinkInputData)
        #
        # ############# BEGIN PROCESSING FOR PATH TWO ##############
        # process_path_two_SINGLE_MAPPING()
        #
        # print("STARTING CREATION OF FAILURE PROBABILITY OUTPUT FILES\n")
        # CreateOutputData.output_file_PATH_TWO(GLOBAL_SINGLE_OUTPUT_FILE_PATH_TWO, CREATE_NUM_REQUESTS, CREATE_NUM_NODES, CREATE_NUM_LINKS)

    if CONSTANTS.GLOBAL_PROTOCOL == 3:
        print("Begin Processing requests using: 'Head vs. Wall' Protocol\n")
        process_path_one_MULTI_MAPPING()
        print("ALL DONE FINDING FIRST PATHS\n")
        print("STARTING CREATION OF OUTPUT FILES\n")
        CreateOutputData.output_file_PATH_ONE(GLOBAL_MULTI_OUTPUT_FILE_PATH_ONE, CREATE_NUM_REQUESTS, CREATE_NUM_NODES, CREATE_NUM_LINKS)
        print("CREATED PATH ONE OUTPUT FILES\n")

        # for link in NodeObj.StaticLinkList:
        #     del link
        # NodeObj.StaticLinkList.clear()
        #
        # for node in NodeObj.StaticNodeList:
        #     del node
        # NodeObj.StaticNodeList.clear()
        #
        # ProcessInputData.processInputDataNode(ProcessInputData.NodeInputData)
        # ProcessInputData.processInputDataLink(ProcessInputData.LinkInputData)

        ############# BEGIN PROCESSING FOR PATH TWO ##############
    if CONSTANTS.GLOBAL_PROTOCOL == 4:
        process_path_two_MULTI_MAPPING()
        print("ALL DONE FINDING SECOND PATHS\n")
        print("STARTING CREATION OF FAILURE PROBABILITY OUTPUT FILES\n")
        CreateOutputData.output_file_PATH_TWO(GLOBAL_MULTI_OUTPUT_FILE_PATH_TWO, CREATE_NUM_REQUESTS, CREATE_NUM_NODES, CREATE_NUM_LINKS)

    # print("CREATING LINE GRAPHS WITH AVAILABLE DATA")
    # run_output_graphs()
