from src import ProcessInputData
from src.NodeObj import NodeObj
from src.Request import Request
from src.PathObj import PathObj
from src.RegionObj import RegionObj
import CreateOutputData
from src.CreateOutputData import output_file_PATH_TWO
from src.ControlPanel import GLOBAL_REQUEST_DELAY_THRESHOLD
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

REQUEST_DELAY_THRESHOLD = GLOBAL_REQUEST_DELAY_THRESHOLD

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


def create_regions():
    regionBounds = [[1, 25], [26, 50], [51, 75], [76, 100], [101, 25], [126, 150]]
    for i in range(5):
        cnt = i+1
        new_region = RegionObj(cnt, 'A', [regionBounds[i][0], regionBounds[i][1]], [], 0)

    for node in NodeObj.StaticNodeList:
        RegionObj.assign_region(node)


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

    path_one_delays = []
    path_two_delays = []

    path_one_avg = []
    path_two_avg = []

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_ONE
        if obj is not None:
            path_one_delays.append(obj.DELAY)

    count = 0
    total_delay_a = 0
    for delay in path_one_delays:
        count += 1
        total_delay_a += delay
        current_delay = total_delay_a / count
        path_one_avg.append(current_delay)

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_TWO
        if obj is not None:
            path_two_delays.append(obj.DELAY)

    cnt = 0
    total_delay_b = 0
    for delay in path_two_delays:
        cnt += 1
        total_delay_b += delay
        current_delay = total_delay_b / cnt
        path_two_avg.append(current_delay)

    plt.axis([1, 200, 1, 300])
    plt.plot(path_one_delays, color='b')
    plt.plot(path_one_avg, color='g')
    plt.plot(path_two_delays, color='r')
    plt.plot(path_two_avg, color='y')
    plt.show()


def create_figure_TWO():
    plt.title("FIGURE 2: Number of incoming requests vs. Average cost per request")
    plt.xlabel("Number of incoming requests")
    plt.ylabel("Average cost per request")

    path_one_costs = []
    path_two_costs = []

    path_one_avg = []
    path_two_avg = []

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_ONE
        if obj is not None:
            path_one_costs.append(obj.COST)

    count = 0
    total_cost_a = 0
    for cost in path_one_costs:
        count += 1
        total_cost_a += cost
        current_cost = total_cost_a / count
        path_one_avg.append(current_cost)

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_TWO
        if obj is not None:
            path_two_costs.append(obj.COST)

    cnt = 0
    total_cost_a = 0
    for cost in path_two_costs:
        cnt += 1
        total_cost_a += cost
        current_cost = total_cost_a / cnt
        path_two_avg.append(current_cost)

    plt.axis([1, 300, 1, 300])
    plt.plot(path_one_costs, color='b')
    plt.plot(path_one_avg, color='g')
    plt.plot(path_two_costs, color='r')
    plt.plot(path_two_avg, color='y')
    plt.show()


def create_figure_THREE():
    plt.title("FIGURE 3: Number of incoming requests vs. Saturation Rate of the Network")
    plt.xlabel("Number of incoming requests")
    plt.ylabel("Number of failed requests")

    po_count = 0
    num_failed_po = 0
    path_one_avg = []

    pt_count = 0
    num_failed_pt = 0
    path_two_avg = []

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_ONE
        po_count += 1
        if obj is None:
            num_failed_po += 1
        else:
            if num_failed_po > 0:
                avg_num_failed = po_count / num_failed_po
                path_one_avg.append(avg_num_failed)

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_TWO
        po_count += 1
        if obj is None:
            num_failed_pt += 1
        else:
            if num_failed_pt > 0:
                avg_num_failed = pt_count / num_failed_pt
                path_two_avg.append(avg_num_failed)


    plt.axis([1, 150, 1, 150])
    plt.plot(path_one_avg, color='b')
    plt.plot(path_two_avg, color='r')
    plt.show()


def create_figure_FOUR():
    plt.title("FIGURE 4: Number of incoming requests vs. FAILURE_RATES_OF_NODES_OVER_TIME")
    plt.xlabel("Number of incoming requests")
    plt.ylabel("Failure rates of nodes over time")

    path_one_failures = []
    path_two_failures = []

    path_one_avg = []
    path_two_avg = []

    current_node_failures = 0
    req_num = 0

    for request in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = request.PATH_ONE
        if obj is not None:
            for node in NodeObj.StaticNodeList:
                req_num += 1
                node.get_status()
                if node.status != "A":
                    current_node_failures += 1
                    path_one_failures.append(current_node_failures)
                    path_one_avg.append(current_node_failures/req_num)

    current_node_failures = 0
    req_num = 0

    for request in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = request.PATH_TWO
        if obj is not None:
            for node in NodeObj.StaticNodeList:
                req_num += 1
                node.get_status()
                if node.status != "A":
                    current_node_failures += 1
                    path_two_failures.append(current_node_failures)
                    path_two_avg.append(current_node_failures/req_num)

    plt.axis([1, 150, 1, 300])
    plt.plot(path_one_failures, color='b')
    plt.plot(path_one_avg, color='g')
    plt.plot(path_two_failures, color='r')
    plt.plot(path_two_avg, color='y')
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
    # create_regions()
    print("INPUT DATA PROCESSED\n")

    set_edges()
    GRAPH.add_edges_from(edges)

    # Just commented out so I don't have to keep closing the window every time
    nx.draw(GRAPH, with_labels=True, font_weight='bold')
    plt.show()  # ToDo Need to figure out why I need this in order to stop the graph from disappearing

    find_isolated_nodes()

    ############ SETUP IS NOW OVER WE CAN BEGIN PROCESSING ##############
    process_path_one()
    print("ALL DONE FINDING FIRST PATHS\n")
    for op in PathObj.StaticOptimalPathsList:
        print(op)

    print("STARTING CREATION OF OUTPUT FILES\n")
    CreateOutputData.output_file_PATH_ONE()
    print("CREATED PATH ONE OUTPUT FILES\n")
    #########################################################

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
    # create_figure_FOUR()
