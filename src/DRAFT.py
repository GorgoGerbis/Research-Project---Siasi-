"""
IGNORE THIS FILE...
THIS IS A BLANK CANVAS TO FOR CLEANING UP NEW FUNCTIONS/METHODS IN AN EASIER TO MANAGE/READ ENVIRONMENT
"""
import os
import random

from src import CONSTANTS
from src.VNFObj import VNFObj

from src.CONSTANTS import NodeInputData, DATASET, CREATE_NUM_REQUESTS, NETWORK_TOPOLOGY, topologyResourcesFolder
from src.CONSTANTS import LinkInputData
from src.CONSTANTS import RequestInputData

from src.CONSTANTS import CREATE_NUM_NODES as NUM_NODES
from src.CONSTANTS import CREATE_NUM_LINKS as NUM_LINKS
from src.CONSTANTS import CREATE_NUM_REQUESTS as NUM_REQS
from src.CONSTANTS import CREATE_NUM_TERMINALS as NUM_TERMINALS
from src.CONSTANTS import MAX_LINKS_PER_NODE, MAX_LINKS_PER_TERMINAL


def create_terminal_and_node_input_data(all_nodes_list, number_of_nodes, number_of_terminals):
    total_to_be_created = number_of_nodes + number_of_terminals

    status = ["N", "T"]  # Status of the node

    with open(NodeInputData, 'w') as fp:
        heading = "NodeId;Status;Resources[CPU, MEM(RAM)];ProcessingDelay;NodeCost;PercentFailure\n"
        fp.write(heading)

        for region in all_nodes_list:
            region_num = region[0]
            list_of_nodes_in_region = region[1]
            for n in list_of_nodes_in_region:
                nodeID = n
                stat = status[0]
                resources = CONSTANTS.node_resources
                processing_delay = CONSTANTS.get_processing_delay(region_num)
                nodeCost = CONSTANTS.get_node_cost()  # random.randint(5, 10) / 10
                pf = CONSTANTS.get_node_fail(region_num)  # random.randint(1, 75) / 100  # Dividing to make them decimals
                nodeLine = "{};{};{};{};{};{}\n".format(nodeID, stat, resources, processing_delay, nodeCost, pf)
                fp.write(nodeLine)

        for cnt in range(number_of_nodes+1, total_to_be_created+1):
            nodeID = cnt + 1  # Ensures we have the correct number for the node
            stat = status[1]
            resources = [0, 0]
            processing_delay = CONSTANTS.get_processing_delay(0)
            nodeCost = CONSTANTS.get_node_cost()  # random.randint(5, 10) / 10
            pf = 0  # CONSTANTS.get_node_fail()  # random.randint(1, 75) / 100  # Dividing to make them decimals
            nodeLine = "{};{};{};{};{};{}\n".format(nodeID, stat, resources, processing_delay, nodeCost, pf)
            fp.write(nodeLine)


def create_link_input_data(r1, r2, r3, r4, num_nodes, num_terminals, max_links_per_terminal):   # num_terminals, num_nodes, num_links, max_links_per_terminal, max_links_per_node
    mega_list = [x for x in r1]

    for x in r2:
        mega_list.append(x)
    for x in r3:
        mega_list.append(x)
    for x in r4:
        mega_list.append(x)

    existing_terminal_links = create_link_duos_TERMINALS(num_terminals, num_nodes, max_links_per_terminal)
    existing_node_links = [x for x in mega_list]
    # existing_node_links = create_link_duos_NODES(num_terminals, num_nodes, num_links, max_links_per_node)

    count = 0

    with open(LinkInputData, 'w') as fp:
        heading = "Link ID;Source;Destination;Bandwidth;EdgeDelay;EdgeCost;failure probability\n"
        fp.write(heading)

        for i, val in enumerate(r1):
            linkID = count + 1
            src = val[0]
            dest = val[1]
            bw = CONSTANTS.link_bandwidth
            ed = CONSTANTS.get_edge_delay(1)
            ec = CONSTANTS.get_edge_cost()
            link_failure = CONSTANTS.get_link_fail(1)
            linkLine = "{};{};{};{};{};{};{}\n".format(linkID, src, dest, bw, ed, ec, link_failure)
            count += 1
            fp.write(linkLine)

        for i, val in enumerate(r2):
            linkID = count + 1
            src = val[0]
            dest = val[1]
            bw = CONSTANTS.link_bandwidth
            ed = CONSTANTS.get_edge_delay(2)
            ec = CONSTANTS.get_edge_cost()
            link_failure = CONSTANTS.get_link_fail(2)
            linkLine = "{};{};{};{};{};{};{}\n".format(linkID, src, dest, bw, ed, ec, link_failure)
            count += 1
            fp.write(linkLine)

        for i, val in enumerate(r3):
            linkID = count + 1
            src = val[0]
            dest = val[1]
            bw = CONSTANTS.link_bandwidth
            ed = CONSTANTS.get_edge_delay(3)
            ec = CONSTANTS.get_edge_cost()
            link_failure = CONSTANTS.get_link_fail(3)
            linkLine = "{};{};{};{};{};{};{}\n".format(linkID, src, dest, bw, ed, ec, link_failure)
            count += 1
            fp.write(linkLine)

        for i, val in enumerate(r4):
            linkID = count + 1
            src = val[0]
            dest = val[1]
            bw = CONSTANTS.link_bandwidth
            ed = CONSTANTS.get_edge_delay(4)
            ec = CONSTANTS.get_edge_cost()
            link_failure = CONSTANTS.get_link_fail(4)
            linkLine = "{};{};{};{};{};{};{}\n".format(linkID, src, dest, bw, ed, ec, link_failure)
            count += 1
            fp.write(linkLine)

        for i, val in enumerate(existing_terminal_links):
            linkID = count + 1
            src = val[0]
            dest = val[1]
            bw = CONSTANTS.link_bandwidth
            ed = CONSTANTS.get_edge_delay(0)
            ec = CONSTANTS.get_edge_cost()
            link_failure = 0  # CONSTANTS.get_link_fail()
            linkLine = "{};{};{};{};{};{};{}\n".format(linkID, src, dest, bw, ed, ec, link_failure)
            count += 1
            fp.write(linkLine)

    get_isolated_and_excess(existing_terminal_links, num_nodes + 1, num_nodes + num_terminals)
    get_isolated_and_excess(existing_node_links, 1, num_nodes)

    return existing_terminal_links, existing_node_links


def create_terminal_requests(number_of_requests, number_of_terminals, number_of_nodes, request_file_data):
    with open(request_file_data, 'w') as fp:
        heading = "requestID;source;destination;Requested VNFs;Requested Bandwidth;Requested VNF failure-threshold\n"
        fp.write(heading)

        for cnt in range(number_of_requests):
            reqID = cnt + 1  # Ensures we have the correct number for the request
            src, dst = HELPER_check_redundancy(number_of_nodes+1, number_of_terminals+number_of_nodes)  # SOURCE AND DESTINATION SHOULD ONLY BE OTHER TERMINALS
            requested_num_func = CONSTANTS.get_VNFs()  # random.randint(1, 6)  # Random amount of functions
            outputFunctions = []  # The random list of functions

            for i in range(requested_num_func):
                while True:
                    current_func = VNFObj.RANDOM
                    name = current_func.name
                    if name not in outputFunctions:
                        outputFunctions.append(name)
                        i += 1
                        break

            requestedBW = get_requested_bandwidth(outputFunctions)  # random.randint(5, 25)
            request_failure_threshold = get_request_failure_threshold(outputFunctions) * 100  # 0

            requestLine = "{};{};{};{};{};{}\n".format(reqID, src, dst, outputFunctions, requestedBW,  request_failure_threshold)
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
    terminal_destination = num_nodes + 1  # Counting upwards for each terminal starting at 1

    for source in range(1, num_nodes):
        for i in range(max_links_per_terminal_node):  # Needs to be the number of terminals per node(source)
            terminal_link_coords = (source, terminal_destination)
            if (terminal_link_coords not in existing_terminal_links) and (source != terminal_destination):
                existing_terminal_links.add(terminal_link_coords)
                terminal_destination += 1

    return existing_terminal_links


def create_link_duos_NODES(num_terminals, num_nodes, num_links, max_links_per_node):
    existing_links = set()
    available_nodes = [x for x in range(1, (num_nodes + 1))]
    already_added = []
    count = 0

    while count < num_links:  # count < 100: # len(existing_links) < num_links OR len(available_nodes) > 0
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

    if start != 1:
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
        if len(isolated) > 0:
            for x in output_excess_links:
                print(f"{item} WITH EXCESS LINKS: [{x[0]}, {x[1]}]")

    # return isolated, output_low_links, output_excess_links


def get_requested_bandwidth(funcs):
    total_bandwidth = 0

    for f in funcs:
        func_num = int(f[1])

        if func_num == 1:
            total_bandwidth += 1

        if func_num == 2:
            total_bandwidth += 2

        if func_num == 3:
            total_bandwidth += 3

        if func_num == 4:
            total_bandwidth += 4

        if func_num == 5:
            total_bandwidth += 5

        if func_num == 6:
            total_bandwidth += 6

    return total_bandwidth


def get_request_failure_threshold(funcs):  # @ToDo should experiment with this.
    """
    GOING TO BE PLAYING WITH THIS ONE SHOULD EXPERIMENT WITH WHAT WORKS BEST
    MEANINGLESS CURRENTLY UNTIL I MAKE EVERY REQUEST DEPENDENT ON ITS OWN FAILURE THRESHOLD.

    EITHER, add up total failure thresholds and average them out.
    OR, TAKE THE HIGHEST THRESHOLD.

    :param funcs:
    :return:
    """
    total_failure = 100.0

    for f in funcs:
        func = VNFObj.retrieve_function_value(f)
        func_fail = func.value[2]

        if func_fail < total_failure:
            total_failure = func_fail

    return total_failure


def HELPER_check_redundancy(start, end):
    while True:
        src = random.randint(start, end)
        dst = random.randint(start, end)

        if src == dst:
            continue
        else:
            return src, dst


def create_topology_layered_regions(region_parameters):
    layer_nodes_list = [[x] for x in range(1, len(region_parameters) + 1)]

    count = 0
    itr = 0
    for num in region_parameters:
        temp = [x + count for x in range(1, num + 1)]
        count += len(temp)
        layer_nodes_list[itr].append(temp)
        itr += 1

    # We now have layer_list complete
    layer_one = create_region_layer_links(layer_nodes_list[0], layer_nodes_list[1])
    layer_two = create_region_layer_links(layer_nodes_list[1], layer_nodes_list[2])
    layer_three = create_region_layer_links(layer_nodes_list[2], layer_nodes_list[3])
    layer_four = create_region_layer_links(layer_nodes_list[3], None)

    return layer_nodes_list, layer_one, layer_two, layer_three, layer_four


def create_region_layer_links(layer_list, connecting_layer):
    layer_duos = []
    num_range = layer_list[1]

    itr = 0
    while itr < len(num_range):
        current_source = num_range[itr]
        left = num_range[itr - 1]
        right = num_range[itr + 1]
        layer_duos.append([current_source, left])
        layer_duos.append([current_source, right])
        itr += 2

    if connecting_layer:
        connecting_num_range = connecting_layer[1]
        itr = 0
        fast_itr = 0
        while itr < len(num_range):
            current_source = num_range[itr]
            next_layer_left = connecting_num_range[fast_itr]
            next_layer_right = connecting_num_range[fast_itr+1]
            layer_duos.append([current_source, next_layer_left])
            layer_duos.append([current_source, next_layer_right])
            itr += 1
            fast_itr += 2

    return layer_duos


if __name__ == '__main__':
    dataset_num = 0
    dataset_num += DATASET

    nn = 150
    nt = 450
    nl = 560

    num_nodes_per_layer = [10, 20, 40, 80]  # Number of nodes per layer....
    all_nodes_per_region, l1, l2, l3, l4 = create_topology_layered_regions(num_nodes_per_layer)
    create_terminal_and_node_input_data(all_nodes_per_region, nn, nt)
    create_link_input_data(l1, l2, l3, l4, nn, nt, 4)

    create_terminal_requests(NUM_REQS, nt, nn, RequestInputData)
    print(f"CREATED REQUEST FILE {dataset_num}")

    RequestInputData = os.path.join(topologyResourcesFolder, "N{}D{}_RequestInputData_{}.txt".format(NETWORK_TOPOLOGY, DATASET + 1, CREATE_NUM_REQUESTS))
    create_terminal_requests(NUM_REQS, nt, nn, RequestInputData)
    print(f"CREATED REQUEST FILE {dataset_num + 1}")

    RequestInputData = os.path.join(topologyResourcesFolder, "N{}D{}_RequestInputData_{}.txt".format(NETWORK_TOPOLOGY, DATASET + 2, CREATE_NUM_REQUESTS))
    create_terminal_requests(NUM_REQS, nt, nn, RequestInputData)
    print(f"CREATED REQUEST FILE {dataset_num + 2}")

    RequestInputData = os.path.join(topologyResourcesFolder, "N{}D{}_RequestInputData_{}.txt".format(NETWORK_TOPOLOGY, DATASET + 3, CREATE_NUM_REQUESTS))
    create_terminal_requests(NUM_REQS, nt, nn, RequestInputData)
    print(f"CREATED REQUEST FILE {dataset_num + 3}")

    RequestInputData = os.path.join(topologyResourcesFolder, "N{}D{}_RequestInputData_{}.txt".format(NETWORK_TOPOLOGY, DATASET + 4, CREATE_NUM_REQUESTS))
    create_terminal_requests(NUM_REQS, nt, nn, RequestInputData)
    print(f"CREATED REQUEST FILE {dataset_num + 4}")
