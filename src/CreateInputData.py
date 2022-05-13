import os
import random
from src.NodeObj import NodeObj
from src.FuncObj import FuncObj

from src.CONSTANTS import NodeInputData
from src.CONSTANTS import LinkInputData
from src.CONSTANTS import RequestInputData

from src.CONSTANTS import GLOBAL_NODE_RESOURCES
from src.CONSTANTS import GLOBAL_LINK_BANDWIDTH
from src.CONSTANTS import GLOBAL_REQUEST_DELAY_THRESHOLD
baseFolder = r"C:\Users\jacks\OneDrive\Desktop\Siasi Research\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")

#NEW STUFF
csv_data = os.path.join(resourcesFolder, "model2.csv")


def createNodeInputData(number_of_nodes):
    status = ["A", "I", "R", "O"]  # Status of the node

    with open(NodeInputData, 'w') as fp:
        heading = "NodeId;Status;Resources[Memory, CPU];ProcessingDelay;NodeCost;PercentFailure\n"
        fp.write(heading)

        for cnt in range(number_of_nodes):
            nodeID = cnt + 1  # Ensures we have the correct number for the node
            stat = status[0]
            resources = [64, 50]    # <-- Based on paper 2 [64gb mem, 50 cpu] # GLOBAL_NODE_RESOURCES  # [100, 100, 100] == [CPU, RAM, Physical Buffer size]
            processing_delay = random.randint(1, 10) / 10    # <-- 1 ms
            nodeCost = random.randint(5, 10) / 10

            # @ToDo Need to come up with ideal failure solution
            pf = random.randint(1, 100) / 100  # Dividing to make them decimals

            nodeLine = "{};{};{};{};{};{}\n".format(nodeID, stat, resources, processing_delay, nodeCost, pf)
            fp.write(nodeLine)


def createLinkInputData(duos):
    with open(LinkInputData, 'w') as fp:
        heading = "Link ID;Source;Destination;Bandwidth;EdgeDelay;EdgeCost;failure probability\n"
        fp.write(heading)

        for i, duo in enumerate(duos):
            linkID = i + 1
            src = duos[i][0]
            dest = duos[i][1]

            bw = GLOBAL_LINK_BANDWIDTH
            ed = random.randint(75, 300) / 100      # Dividing to make them decimals
            ec = 1.5    # Based off of paper 2 averages

            # @ToDo Need to come up with ideal failure solution
            link_failure = random.randint(1, 100) / 100     # Dividing to make them decimals

            linkLine = "{};{};{};{};{};{};{}\n".format(linkID, src, dest, bw, ed, ec, link_failure)
            fp.write(linkLine)


def createRequests(number_of_requests, number_of_nodes):
    with open(RequestInputData, 'w') as fp:
        heading = "requestID;source;destination;Requested VNFs;Requested Bandwidth\n"
        fp.write(heading)

        for cnt in range(number_of_requests):
            reqID = cnt + 1  # Ensures we have the correct number for the request

            src, dst = HELPER_check_redundancy(number_of_nodes)

            requested_num_func = 3  # random.randint(1, 6)  # Random amount of functions
            outputFunctions = []  # The random list of functions
            requestedBW = 0 # @ToDo Maybe we should be adjusting this to match their num_funcs

            for i in range(requested_num_func):
                while True:
                    current_func = FuncObj.RANDOM
                    name = current_func.name
                    temp = current_func.value
                    if name not in outputFunctions:
                        outputFunctions.append(name)
                        requestedBW += temp[2]
                        i += 1
                        break

            requestLine = "{};{};{};{};{}\n".format(reqID, src, dst, outputFunctions, requestedBW)
            fp.write(requestLine)


def HELPER_import_csv_data(filepath):
    output = []
    with open(filepath) as fp:
        fp.readline()  # <-- This is so that it skips the first line
        for cnt, line in enumerate(fp):
            if (line == "\n") or (line == ""):
                continue
            else:
                line = line.strip('\n')
                currentElements = line.split(',')
                currentElements.pop(0)  # <--- remove first item in currentElements
                currentElements = list(map(int, currentElements))     # <--- Convert str -> int

                for i, row in enumerate(currentElements):
                    duo = []
                    if row == 1:
                        duo.append(cnt+1)
                        duo.append(i+1)
                        print("NODE: D{}, ADJACENT NODES:{}".format(cnt + 1, duo))

                        x = duo[0]
                        y = duo[1]
                        if [x, y] not in output and [y, x] not in output:
                            output.append(duo)
    return output


def HELPER_check_redundancy(num_nodes):
    while True:
        src = random.randint(1, num_nodes)
        dst = random.randint(1, num_nodes)

        if src == dst:
            continue
        else:
            return src, dst


if __name__ == '__main__':
    num_nodes = 16
    num_links = 24
    num_requests = 100

    adj_duos = HELPER_import_csv_data(csv_data)

    print("CREATING NEW INPUT DATA!\n")
    print("TOTAL NODES: {} TOTAL LINKS: {} TOTAL REQUESTS: {}\n".format(num_nodes, num_links, num_requests))
    createNodeInputData(num_nodes)
    createLinkInputData(adj_duos)
    createRequests(num_requests, num_nodes)
    print("FINISHED CREATING INPUT DATA\n")
