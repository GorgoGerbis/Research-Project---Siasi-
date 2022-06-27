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
from src.CONSTANTS import CREATE_NUM_TERMINALS as NUM_TERMINALS
from src.CONSTANTS import MAX_LINKS_PER_NODE, MAX_LINKS_PER_TERMINAL


def create_terminal_and_node_input_data(number_of_nodes, number_of_terminals):
    """
    Create and write to the NodeInputData File
    :param number_of_terminals:
    :param number_of_nodes: Int number of nodes to create...
    :return:
    """
    total_to_be_created = number_of_terminals + number_of_nodes
    status = ["N", "T"]  # Status of the node

    with open(NodeInputData, 'w') as fp:
        heading = "NodeId;Status;Resources[CPU, MEM(RAM)];ProcessingDelay;NodeCost;PercentFailure\n"
        fp.write(heading)

        for cnt in range(total_to_be_created):
            nodeID = cnt + 1  # Ensures we have the correct number for the node

            if cnt < number_of_terminals:  # CREATE TERMINALS
                stat = status[1]
                resources = [0, 0]
                processing_delay = CONSTANTS.get_processing_delay()
                nodeCost = CONSTANTS.get_node_cost()  # random.randint(5, 10) / 10
                pf = 0  # CONSTANTS.get_node_fail()  # random.randint(1, 75) / 100  # Dividing to make them decimals
                nodeLine = "{};{};{};{};{};{}\n".format(nodeID, stat, resources, processing_delay, nodeCost, pf)
                fp.write(nodeLine)
            else:
                stat = status[0]
                resources = CONSTANTS.node_resources
                processing_delay = CONSTANTS.get_processing_delay()
                nodeCost = CONSTANTS.get_node_cost()  # random.randint(5, 10) / 10
                pf = CONSTANTS.get_node_fail()  # random.randint(1, 75) / 100  # Dividing to make them decimals
                nodeLine = "{};{};{};{};{};{}\n".format(nodeID, stat, resources, processing_delay, nodeCost, pf)
                fp.write(nodeLine)


def create_link_input_data(num_terminals, num_nodes, num_links, max_links_per_terminal, max_links_per_node):
    existing_terminal_links = create_link_duos_TERMINALS(num_terminals, num_nodes, max_links_per_terminal)
    existing_node_links = create_link_duos_NODES(num_terminals, num_nodes, num_links, max_links_per_node)

    get_isolated_and_excess(existing_terminal_links, 1, num_terminals)
    get_isolated_and_excess(existing_node_links, num_terminals+1, num_terminals+num_nodes)

    count = 0

    with open(LinkInputData, 'w') as fp:
        heading = "Link ID;Source;Destination;Bandwidth;EdgeDelay;EdgeCost;failure probability\n"
        fp.write(heading)

        for i, val in enumerate(existing_terminal_links):
            linkID = count + 1
            src = val[0]
            dest = val[1]
            bw = CONSTANTS.link_bandwidth
            ed = CONSTANTS.get_edge_delay()
            ec = CONSTANTS.get_edge_cost()
            link_failure = CONSTANTS.get_link_fail()
            linkLine = "{};{};{};{};{};{};{}\n".format(linkID, src, dest, bw, ed, ec, link_failure)
            count += 1
            fp.write(linkLine)

        for i, val in enumerate(existing_node_links):
            linkID = count + 1
            src = val[0]
            dest = val[1]
            bw = CONSTANTS.link_bandwidth
            ed = CONSTANTS.get_edge_delay()
            ec = CONSTANTS.get_edge_cost()
            link_failure = CONSTANTS.get_link_fail()
            linkLine = "{};{};{};{};{};{};{}\n".format(linkID, src, dest, bw, ed, ec, link_failure)
            count += 1
            fp.write(linkLine)

    return existing_terminal_links, existing_node_links


def create_terminal_requests(number_of_requests, number_of_terminals):
    with open(RequestInputData, 'w') as fp:
        heading = "requestID;source;destination;Requested VNFs;Requested Bandwidth;Requested VNF failure-threshold\n"
        fp.write(heading)

        for cnt in range(number_of_requests):
            reqID = cnt + 1  # Ensures we have the correct number for the request
            src, dst = HELPER_check_redundancy(number_of_terminals)     # SOURCE AND DESTINATION SHOULD ONLY BE OTHER TERMINALS
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


def create_link_duos_TERMINALS(num_terminals, num_nodes, max_links_per_terminal_node):
    """
    Create the links that connect the first layer of terminals and fog nodes.
    The first x number of terminals need to be divided into sets/groups of 3 or whatever the max_links_per_terminal_node variabel is equal to.
    Each group of 3 gets assigned to a node.
    :param num_terminals:
    :param num_nodes:
    :param max_links_per_terminal_node:
    :return:
    """
    existing_terminal_links = set()
    terminal_destination = 1    # Counting upwards for each terminal starting at 1

    for source in range(num_terminals+1, num_terminals + num_nodes + 1):
        for i in range(max_links_per_terminal_node):  # Needs to be the number of terminals per node(source)
            terminal_link_coords = (source, terminal_destination)
            if (terminal_link_coords not in existing_terminal_links) and (source != terminal_destination):
                existing_terminal_links.add(terminal_link_coords)
                terminal_destination += 1

    return existing_terminal_links


def create_link_duos_NODES(num_terminals, num_nodes, num_links, max_links_per_node):
    existing_links = set()
    available_nodes = [x for x in range(num_terminals+1, (num_nodes + num_terminals + 1))]
    already_added = []
    count = 0

    while count < num_links:     # count < 100: # len(existing_links) < num_links OR len(available_nodes) > 0
        source, destination = random.choices(available_nodes, k=2)
        link_coords = (source, destination)

        if (link_coords not in existing_links) and (source != destination) and (already_added.count(source) < max_links_per_node and already_added.count(destination) < max_links_per_node):
            existing_links.add(link_coords)
            already_added.append(source)
            already_added.append(destination)
            count += 1

    return existing_links


def search_set(set_data, val):
    mini_count = 0
    for element in set_data:  # Just a small search function
        if val in element:
            mini_count += 1
            print("SRC: {}, DST: {}, COUNT: {}".format(element[0], element[1], mini_count))
    print('')


def get_isolated_and_excess(set_data, start, end):
    isolated = []
    low_links = []
    excess_links = []

    temp_count = 0
    for i in range(start, end + 1):
        for element in set_data:
            if i in element:
                temp_count += 1

        if temp_count == 0:
            isolated.append(i)
        if temp_count <= 2:
            low_links.append([i, temp_count])
        else:
            excess_links.append([i, temp_count])

        temp_count = 0

    output_excess_links = sorted(excess_links, key=lambda l: l[1])
    output_low_links = sorted(low_links, key=lambda l: l[1])

    if start == 1:
        item = "TERMINALS"
        print("CHECKING LINK INPUT DATA")
        if len(isolated) != 0:
            print(f"NUMBER OF ISOLATED {item} = {len(isolated)}, ISOLATED {item}: {isolated}")
            print(f"{item} WITH LOWER LINKS: {output_low_links}\n")
            for x in output_excess_links:
                print(f"{item} WITH EXCESS LINKS: [{x[0]}, {x[1]}]")
        else:
            print(f"NUMBER OF ISOLATED {item} = {len(isolated)}, ISOLATED {item}: {isolated}\n")
    else:
        item = "FOG NODES"
        print("CHECKING LINK INPUT DATA")
        print(f"NUMBER OF ISOLATED {item} = {len(isolated)}, ISOLATED {item}: {isolated}")
        print(f"{item} WITH LOWER LINKS: {output_low_links}\n")
        for x in output_excess_links:
            print(f"{item} WITH EXCESS LINKS: [{x[0]}, {x[1]}]")

    # return isolated, output_low_links, output_excess_links


def HELPER_check_redundancy(num_nodes):
    while True:
        src = random.randint(1, num_nodes)
        dst = random.randint(1, num_nodes)

        if src == dst:
            continue
        else:
            return src, dst


if __name__ == '__main__':
    print("CREATING NEW INPUT DATA!\n")
    print("TOTAL NODES: {} TOTAL TERMINALS: {} TOTAL LINKS: {} TOTAL REQUESTS: {}\n".format(NUM_NODES, NUM_TERMINALS, NUM_LINKS, NUM_REQS))

    # create_terminal_and_node_input_data(NUM_NODES, NUM_TERMINALS)
    #
    # terminal_links, node_links = create_link_input_data(NUM_TERMINALS, NUM_NODES, NUM_LINKS, MAX_LINKS_PER_TERMINAL, MAX_LINKS_PER_NODE)
    # # get_isolated_and_excess(terminal_links, 1, NUM_TERMINALS)  # num_nodes, start, end
    # # get_isolated_and_excess(node_links, NUM_TERMINALS+1, NUM_TERMINALS+NUM_NODES)   # num_nodes, start, end

    create_terminal_requests(NUM_REQS, NUM_TERMINALS)

    print("FINISHED CREATING INPUT DATA\n")

    