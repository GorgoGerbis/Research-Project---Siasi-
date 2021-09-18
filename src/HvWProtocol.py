from src import ProcessInputData
from src.NodeObj import NodeObj
from src.Request import Request
from src.PathObj import PathObj
from src.RegionObj import RegionObj
import CreateOutputData
from src.CreateOutputData import output_file_PATH_TWO

from src.ControlPanel import GLOBAL_NODE_RESOURCES
from src.ControlPanel import GLOBAL_LINK_BANDWIDTH
from src.ControlPanel import GLOBAL_REQUEST_DELAY_THRESHOLD

# Need these for path finding and graphing
import networkx as nx
import matplotlib.pyplot as plt

# Need these to process requests
from src.ProcessPathing import RUN_PATH_ONE
from src.ProcessPathing import RUN_PATH_TWO

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

NODES_THAT_AUTO_FAIL = [5, 6, 13, 19]

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


def fail_unavailable_paths():
    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        if req.requestStatus[0] == 3:
            current_route = req.PATH_ONE.route
            for node in current_route:
                if node in NODES_THAT_AUTO_FAIL:
                    req.requestStatus[0] = 2


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
                PathObj(pathID, path, 0, current_request_data, [], 0, 0, 0, 1)
                count += 1

        RUN_PATH_ONE(req)   # <--- Step 3, 4 and 5 starts here


def process_path_two():
    for req in Request.STATIC_TOTAL_REQUEST_LIST:   # STEP ONE
        print("BEGUN PROCESSING REQUEST: {} Source: {} Destination {} Functions: {}\n".format(req.requestID, req.source, req.destination, req.requestedFunctions))
        if req.source in NODES_THAT_AUTO_FAIL or req.destination in NODES_THAT_AUTO_FAIL:
            req.requestStatus[1] = 2
            continue
        else:
            count = 1  # Needs to be reset to 1 when a new request is being processed
            current_request_data = [req.requestedFunctions, req.request_delay_threshold, req.requestedBW]
            current_request_all_possible_paths = nx.all_simple_paths(GRAPH, req.source, req.destination)

            for path in current_request_all_possible_paths:     # STEP TWO
                if len(path) != 0:
                    pathID = "R{}P{}".format(req.requestID, count)
                    # ToDo should make a static list of all paths being processed for a single request
                    PathObj(pathID, path, 0, current_request_data, [], 0, 0, 0, 2)
                    count += 1

            RUN_PATH_TWO(req)


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
            for step in obj.route:
                if step in NODES_THAT_AUTO_FAIL:
                    continue
                else:
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

    plt.subplot(1, 2, 1)
    plt.axis([1, 300, 1, 40])
    plt.title("Conventional mapping")
    plt.xlabel("Number of processed requests")
    plt.ylabel("Average delay per request")
    plt.plot(path_one_delays, color='g', label="Conventional mapping")
    plt.plot(path_one_avg, color='b', label="Conventional mapping averages")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.axis([1, 300, 1, 40])
    plt.title("Failure-aware mapping")
    plt.xlabel("Number of processed requests")
    plt.ylabel("Average delay per request")
    plt.plot(path_two_delays, color='y', label="Failure-aware mapping")
    plt.plot(path_two_avg, color='r', label="Failure-aware mapping averages")
    plt.legend()
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

    plt.subplot(1, 2, 1)
    plt.axis([1, 300, 1, 200])
    plt.title("Conventional mapping")
    plt.xlabel("Number of processed requests")
    plt.ylabel("Average cost per request")
    plt.plot(path_one_costs, color='g', label="Conventional mapping")
    plt.plot(path_one_avg, color='b', label="Conventional mapping averages")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.axis([1, 300, 1, 200])
    plt.title("Failure-aware mapping")
    plt.xlabel("Number of processed requests")
    plt.ylabel("Average cost per request")
    plt.plot(path_two_costs, color='y', label="Failure-aware mapping")
    plt.plot(path_two_avg, color='r', label="Failure-aware mapping averages")
    plt.legend()
    plt.show()


def create_figure_THREE():
    plt.title("FIGURE 3: Number of incoming requests vs. Success Rate of requests")
    plt.xlabel("Number of incoming requests")
    plt.ylabel("Success rates of requests")

    total_avg = []
    total_avg_two = []
    total_processed_reqs = 0
    passed_requests = 0
    denied_requests = 0

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_ONE
        total_processed_reqs += 1
        if obj is not None:
            for step in obj.route:
                if step in NODES_THAT_AUTO_FAIL:
                    denied_requests += 1
                else:
                    passed_requests += 1
        else:
            denied_requests += 1

        total_avg.append(passed_requests)

    total_processed_reqs = 0
    passed_requests = 0
    denied_requests = 0

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_TWO
        total_processed_reqs += 1
        if obj is not None:
            passed_requests += 1
        else:
            denied_requests += 1

        total_avg_two.append(passed_requests)

    plt.subplot(1, 2, 1)
    plt.axis([0, 300, 0, 300])
    plt.title("Conventional mapping")
    plt.xlabel("Number of processed requests")
    plt.ylabel("Number of successful requests")
    plt.plot(total_avg, color='b', label="Conventional mapping")

    plt.subplot(1, 2, 2)
    plt.axis([0, 300, 0, 300])
    plt.title("Failure aware mapping")
    plt.xlabel("Number of processed requests")
    plt.ylabel("Number of successful requests")
    plt.plot(total_avg_two, color='r', label="Failure-aware mapping")
    plt.show()


def create_figure_FOUR():
    plt.title("FIGURE 4: Number of incoming requests vs. Mean probability of failure")
    plt.xlabel("Number of incoming requests")
    plt.ylabel("Mean probability of failure")

    path_one_fails = []
    path_two_fails = []

    path_one_avg= []
    path_two_avg = []

    path_one_approved = 0
    path_two_approved = 0

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        if req.requestStatus[0] == 3:
            path_one_approved += 1
            obj = req.PATH_ONE
            path_one_fails.append(obj.FAILURE_PROBABILITY)
            path_one_avg.append(obj.FAILURE_PROBABILITY / path_one_approved)

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        if req.requestStatus[1] == 3:
            path_two_approved += 1
            obj = req.PATH_TWO
            path_two_fails.append(obj.FAILURE_PROBABILITY)
            path_two_avg.append(obj.FAILURE_PROBABILITY / path_two_approved)

    plt.subplot(1, 2, 1)
    plt.axis([0, 100, 0, 100])
    plt.title("Failure aware mapping")
    plt.xlabel("Number of processed requests")
    plt.ylabel("Probability of failure")
    plt.plot(path_one_fails, color='b', label="Failure-aware mapping")
    plt.plot(path_one_avg, color='g', label="Failure-aware mapping averages")

    plt.subplot(1, 2, 2)
    plt.axis([0, 100, 0, 100])
    plt.title("Failure aware mapping")
    plt.xlabel("Number of processed requests")
    plt.ylabel("Probability of failure")
    plt.plot(path_two_fails, color='r', label="Failure-aware mapping")
    plt.plot(path_two_avg, color='y', label="Failure-aware mapping averages")
    plt.show()


def create_figure_FIVE(nodes_path_one, nodes_path_two):
    plt.title("FIGURE 5: Number of incoming requests vs. Saturation of Nodes")
    plt.xlabel("Number of incoming requests")
    plt.ylabel("Average node resources remaining")

    DIVISOR = GLOBAL_NODE_RESOURCES[0]

    path_one_avg = []
    path_two_avg = []

    for n in nodes_path_one:
        output = n / DIVISOR
        output = output * 100
        path_one_avg.append(output)

    for n in nodes_path_two:
        output = n / DIVISOR
        output = output * 100
        path_two_avg.append(output)

    plt.axis([0, 100, 0, 100])
    plt.plot(path_one_avg, color='b', label="Conventional mapping")
    plt.plot(path_two_avg, color='r', label="Failure-aware mapping")
    plt.legend()
    plt.show()


def create_figure_SIX(links_path_one, links_path_two):
    plt.title("FIGURE 6: Number of incoming requests vs. Saturation of Links")
    plt.xlabel("Number of incoming requests")
    plt.ylabel("Average link bandwidth remaining")

    path_one_avg = []
    path_two_avg = []

    for l in links_path_one:
        output = l / GLOBAL_LINK_BANDWIDTH
        output = output * 100
        path_one_avg.append(output)

    for l in links_path_two:
        output = l / GLOBAL_LINK_BANDWIDTH
        output = output * 100
        path_two_avg.append(output)

    plt.axis([0, 100, 0, 100])
    plt.plot(path_one_avg, color='b', label="Conventional mapping")
    plt.plot(path_two_avg, color='r', label="Failure-aware mapping")
    plt.legend()
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

    ########### SETUP IS NOW OVER WE CAN BEGIN PROCESSING ##############
    process_path_one()
    print("ALL DONE FINDING FIRST PATHS\n")
    for op in PathObj.StaticOptimalPathsList:
        print(op)

    fail_unavailable_paths()
    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_ONE
        if obj is not None:
            print(obj)

    print("STARTING CREATION OF OUTPUT FILES\n")
    CreateOutputData.output_file_PATH_ONE()
    print("CREATED PATH ONE OUTPUT FILES\n")
    #########################################################

    for link in NodeObj.StaticLinkList:
        del link
    NodeObj.StaticLinkList.clear()

    for node in NodeObj.StaticNodeList:
        del node
    NodeObj.StaticNodeList.clear()

    ProcessInputData.processInputDataNode(ProcessInputData.NodeInputData)
    ProcessInputData.processInputDataLink(ProcessInputData.LinkInputData)

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
    create_figure_FOUR()
    # create_figure_FIVE(NodeObj.StaticNodeResources_PATHONE, NodeObj.StaticNodeResources_PATHTWO)
    # create_figure_SIX(NodeObj.StaticLinkResources_PATHONE, NodeObj.StaticLinkResources_PATHTWO)

