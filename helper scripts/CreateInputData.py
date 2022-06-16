import os
import random

from src import CONSTANTS
from src.VNFObj import VNFObj

from src.CONSTANTS import NodeInputData
from src.CONSTANTS import LinkInputData
from src.CONSTANTS import RequestInputData

from src.CONSTANTS import CREATE_NUM_NODES as NUM_NODES
from src.CONSTANTS import CREATE_NUM_LINKS as NUM_LINKS
from src.CONSTANTS import CREATE_NUM_REQUESTS as NUM_REQS


def createNodeInputData(number_of_nodes):
    """
    Create and write to the NodeInputData File
    :param number_of_nodes: Int number of nodes to create...
    :return:
    """
    status = ["A", "I", "R", "O"]  # Status of the node

    with open(NodeInputData, 'w') as fp:
        heading = "NodeId;Status;Resources[CPU, MEM(RAM)];ProcessingDelay;NodeCost;PercentFailure\n"
        fp.write(heading)

        for cnt in range(number_of_nodes):
            nodeID = cnt + 1  # Ensures we have the correct number for the node
            stat = status[0]
            resources = CONSTANTS.node_resources
            processing_delay = CONSTANTS.get_processing_delay()
            nodeCost = CONSTANTS.get_node_cost()  # random.randint(5, 10) / 10
            pf = CONSTANTS.get_node_fail()  # random.randint(1, 75) / 100  # Dividing to make them decimals
            nodeLine = "{};{};{};{};{};{}\n".format(nodeID, stat, resources, processing_delay, nodeCost, pf)
            fp.write(nodeLine)


def createLinkInputData(num_nodes, num_links):
    existing_links = create_link_duos(num_nodes, 4)

    with open(LinkInputData, 'w') as fp:
        heading = "Link ID;Source;Destination;Bandwidth;EdgeDelay;EdgeCost;failure probability\n"
        fp.write(heading)

        for i, val in enumerate(existing_links):
            linkID = i + 1
            src = val[0]
            dest = val[1]
            bw = CONSTANTS.link_bandwidth
            ed = CONSTANTS.get_edge_delay()
            ec = CONSTANTS.get_edge_cost()
            link_failure = CONSTANTS.get_link_fail()
            linkLine = "{};{};{};{};{};{};{}\n".format(linkID, src, dest, bw, ed, ec, link_failure)
            fp.write(linkLine)


def createRequests(number_of_requests, number_of_nodes):
    with open(RequestInputData, 'w') as fp:
        heading = "requestID;source;destination;Requested VNFs;Requested Bandwidth;Requested VNF failure-threshold\n"
        fp.write(heading)

        for cnt in range(number_of_requests):
            reqID = cnt + 1  # Ensures we have the correct number for the request
            src, dst = HELPER_check_redundancy(number_of_nodes)
            requested_num_func = CONSTANTS.get_VNFs()   # random.randint(1, 6)  # Random amount of functions
            outputFunctions = []  # The random list of functions
            requestedBW = random.randint(5, 25)     # CONSTANTS.get_reqBW()
            request_failure_threshold = 0

            for i in range(requested_num_func):
                while True:
                    current_func = VNFObj.RANDOM
                    name = current_func.name
                    temp = current_func.value
                    if name not in outputFunctions:
                        outputFunctions.append(name)
                        request_failure_threshold += temp[2]
                        i += 1
                        break

            requestLine = "{};{};{};{};{};{}\n".format(reqID, src, dst, outputFunctions, requestedBW, request_failure_threshold)
            fp.write(requestLine)


def create_link_duos(num_nodes, max_links_per_node):
    existing_links = set()
    available_nodes = [x for x in range(1, num_nodes+1)]
    already_added = []
    count = 0

    while count < 100:     # len(existing_links) < num_links OR len(available_nodes) > 0
        source, destination = random.choices(available_nodes, k=2)
        link_coords = (source, destination)

        if (link_coords not in existing_links) and (source != destination) and (already_added.count(source) < max_links_per_node and already_added.count(destination) <= max_links_per_node):
            existing_links.add(link_coords)
            already_added.append(source)
            already_added.append(destination)
            count += 1

    print(existing_links)
    print(len(existing_links))
    return existing_links


def HELPER_check_redundancy(num_nodes):
    while True:
        src = random.randint(1, num_nodes)
        dst = random.randint(1, num_nodes)

        if src == dst:
            continue
        else:
            return src, dst


if __name__ == '__main__':
    # csv_fp = os.path.join(r"C:\Users\jacks\OneDrive\Desktop\Siasi Research\Research-Project---Siasi-\resources\Small Topology", "Small_TOP_Matrix.csv")
    # adj_duos = HELPER_import_csv_data(csv_fp)
    print("CREATING NEW INPUT DATA!\n")
    print("TOTAL NODES: {} TOTAL LINKS: {} TOTAL REQUESTS: {}\n".format(NUM_NODES, NUM_LINKS, NUM_REQS))
    createNodeInputData(NUM_NODES)
    createLinkInputData(NUM_NODES, NUM_LINKS)
    createRequests(NUM_REQS, NUM_NODES)
    print("FINISHED CREATING INPUT DATA\n")
