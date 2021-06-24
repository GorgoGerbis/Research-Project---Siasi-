import os
import random
from src.FuncObj import FuncObj


baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
NodeInputData = os.path.join(resourcesFolder, "NodeInputData-EXSMALL-TEST-6-23-21.csv")
LinkInputData = os.path.join(resourcesFolder, "LinkInputData-EXSMALL-TEST-6-23-21.csv")
auto_requests_Opt = os.path.join(resourcesFolder, "requests-EXSMALL-TEST-6-23-21.txt")
# NodeOpt = os.path.join(resourcesFolder, "NodeInputData-LARGE-TEST-6-18-21.csv")
# LinkOpt = os.path.join(resourcesFolder, "LinkInputData-LARGE-TEST-6-18-21.csv")
# auto_requests_Opt = os.path.join(resourcesFolder, "requests-LARGE-TEST-6-18-21.txt")


def createNodeInputData(number_of_nodes):
    status = ["A", "I", "R", "O"]  # Status of the node

    with open(NodeInputData, 'w') as fp:
        heading = "NodeId;Latitude;Longitude;Status;Resources[CPU Memory Physical Buffer " \
                  "Size];ProcessingDelay;NodeCost;PercentFailure\n"
        fp.write(heading)

        num_range = [20, 30, 40, 50]

        for cnt in range(number_of_nodes):
            nodeID = cnt + 1  # Ensures we have the correct number for the node
            lat = random.randint(60, 940)
            long = random.randint(60, 740)
            stat = status[0]
            pick_one = random.randint(0, 3)
            resources = [num_range[pick_one], num_range[pick_one], num_range[pick_one]]     # [CPU, RAM, Physical Buffer size]
            processing_delay = 1
            nodeCost = 5
            pf = random.randint(1, 50) / 100    # Dividing to make them decimals

            nodeLine = "{};{};{};{};{};{};{};{}\n".format(nodeID, lat, long, stat, resources, processing_delay, nodeCost, pf)
            fp.write(nodeLine)


def createLinkInputData(number_of_links, number_of_nodes):
    with open(LinkInputData, 'w') as fp:
        heading = "Link ID;Source;Destination;Bandwidth;EdgeDelay;EdgeCost;PercentFailure\n"
        fp.write(heading)

        for cnt in range(number_of_links):
            linkID = cnt+1
            src = random.randint(1, number_of_nodes)
            dest = random.randint(1, number_of_nodes)
            bw = 15
            ed = 1 # random.randint(2, 6) / 10  # Dividing to make them decimals
            ec = 5
            link_failure = random.randint(1, 50) / 100  # Dividing to make them decimals

            linkLine = "{};{};{};{};{};{};{}\n".format(linkID, src, dest, bw, ed, ec, link_failure)
            fp.write(linkLine)


def createRequests(number_of_requests, number_of_nodes):
    with open(auto_requests_Opt, 'w') as fp:
        heading = "requestID;source;destination;{function1[r1,r2,r3], Function2[r1,r2,r3], Function3[r1,r2," \
                  "r3]};RequestedBandwidth\n"
        fp.write(heading)

        for cnt in range(number_of_requests):
            reqID = cnt + 1  # Ensures we have the correct number for the node
            src = random.randint(1, number_of_nodes)
            dest = random.randint(1, number_of_nodes)

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


if __name__ == '__main__':

    num_nodes = 24
    num_links = 48
    num_requests = 15

    print("CREATING NEW INPUT DATA!\n")
    print("TOTAL NODES: {} TOTAL LINKS: {} TOTAL REQUESTS: {}\n".format(num_nodes, num_links, num_requests))
    createNodeInputData(num_nodes)
    createLinkInputData(num_links, num_nodes)
    createRequests(num_requests, num_nodes)
    print("FINISHED CREATING INPUT DATA\n")
