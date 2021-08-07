import os
import random
from src.NodeObj import NodeObj
from src.FuncObj import FuncObj

from src.ControlPanel import NodeInputData
from src.ControlPanel import LinkInputData
from src.ControlPanel import RequestInputData


def createNodeInputData(number_of_nodes):
    status = ["A", "I", "R", "O"]  # Status of the node

    with open(NodeInputData, 'w') as fp:
        heading = "NodeId;Latitude;Longitude;Status;Resources[CPU Memory Physical Buffer " \
                  "Size];ProcessingDelay;NodeCost;PercentFailure\n"
        fp.write(heading)

        for cnt in range(number_of_nodes):
            nodeID = cnt + 1  # Ensures we have the correct number for the node
            lat = random.randint(60, 940)
            long = random.randint(60, 940)
            stat = status[0]
            resources = [60, 60, 60] # [CPU, RAM, Physical Buffer size]
            processing_delay = 1
            nodeCost = 5
            pf = random.randint(1, 55) / 100    # Dividing to make them decimals

            nodeLine = "{};{};{};{};{};{};{};{}\n".format(nodeID, lat, long, stat, resources, processing_delay, nodeCost, pf)
            fp.write(nodeLine)


def createLinkInputData(number_of_links, num_nodes):
    temp_list = []

    with open(LinkInputData, 'w') as fp:
        heading = "Link ID;Source;Destination;Bandwidth;EdgeDelay;EdgeCost;PercentFailure\n"
        fp.write(heading)

        link_list = create_pair(number_of_links, num_nodes, temp_list)

        for i, duo in enumerate(link_list):
            linkID = i+1
            src = link_list[i][0]
            dest = link_list[i][1]

            bw = 35
            ed = 1 # random.randint(2, 6) / 10  # Dividing to make them decimals
            ec = 5
            link_failure = random.randint(1, 55) / 100  # Dividing to make them decimals

            linkLine = "{};{};{};{};{};{};{}\n".format(linkID, src, dest, bw, ed, ec, link_failure)
            fp.write(linkLine)


def createRequests(number_of_requests, number_of_nodes):
    with open(RequestInputData, 'w') as fp:
        heading = "requestID;source;destination;{function1[r1,r2,r3], Function2[r1,r2,r3], Function3[r1,r2," \
                  "r3]};RequestedBandwidth\n"
        fp.write(heading)

        for cnt in range(number_of_requests):
            reqID = cnt + 1  # Ensures we have the correct number for the node

            src, dest = not_the_same(number_of_nodes)

            if dest == src:
                dest = random.randint(1, number_of_nodes)

            requested_num_func = random.randint(1, 6)  # Random amount of functions
            requestedBW = 5
            outputFunctions = []    # The random list of functions

            for i in range(requested_num_func):
                if i <= requested_num_func:
                    current_func = FuncObj.RANDOM
                    current_func = current_func.name
                    if current_func not in outputFunctions:
                        outputFunctions.append(current_func)
                i += 1

            requestLine = "{};{};{};{};{}\n".format(reqID, src, dest, outputFunctions, requestedBW)
            fp.write(requestLine)


def create_pair(num_links, num_nodes, output):
    while len(output) < num_links:
        src = random.randint(1, num_nodes)
        dest = random.randint(1, num_nodes)
        temp = [src, dest]
        if temp not in output:
            output.append(temp)

    return output


def not_the_same(num_nodes):
    con = True
    while con:
        src = random.randint(1, num_nodes)
        dest = random.randint(1, num_nodes)

        if src != dest:
            con = False
            return src, dest


if __name__ == '__main__':
    num_nodes = 24 # 12
    num_links = 48 # 24
    num_requests = 100 # 48

    print("CREATING NEW INPUT DATA!\n")
    print("TOTAL NODES: {} TOTAL LINKS: {} TOTAL REQUESTS: {}\n".format(num_nodes, num_links, num_requests))
    createNodeInputData(num_nodes)
    createLinkInputData(num_links, num_nodes)
    createRequests(num_requests, num_nodes)
    print("FINISHED CREATING INPUT DATA\n")
