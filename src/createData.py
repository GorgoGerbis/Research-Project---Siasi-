import os
import random
from src.FuncObj import FuncObj
# This script just makes data for me to play with


baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
NodeInputData = os.path.join(resourcesFolder, "NodeInputData5-EXSMALL-5-17-21.csv")
LinkInputData = os.path.join(resourcesFolder, "LinkInputData-EXSMALL-5-17-21.csv")
auto_requests_Opt = os.path.join(resourcesFolder, "requests-EXSMALL-5-17-21.txt")


def createNodeInputData(number_of_nodes):
    status = ["A", "I", "R", "O"]  # Status of the node
    physical_buffer_size = [10, 20, 30, 40, 50]

    with open(NodeInputData, 'w') as fp:
        heading = "NodeId;Latitude;Longitude;Status;Resources[CPU Memory Physical Buffer " \
                  "Size];ProcessingDelay;NodeCost\n"
        fp.write(heading)

        for cnt in range(number_of_nodes):
            nodeID = cnt + 1  # Ensures we have the correct number for the node
            lat = random.randint(60, 940)
            long = random.randint(60, 740)
            stat = status[random.randint(0, 3)]

            cpu = random.randint(0, 100)
            mem = random.randint(0, 100)
            pbs = physical_buffer_size[random.randint(0, 4)]

            resources = [cpu, mem, pbs]
            processing_delay = random.randint(0, 100)
            nodeCost = random.randint(1, 5)

            nodeLine = "{};{};{};{};{};{};{}\n".format(nodeID, lat, long, stat, resources, processing_delay, nodeCost)
            fp.write(nodeLine)


def createLinkInputData(number_of_links, number_of_nodes):
    with open(LinkInputData, 'w') as fp:
        heading = "Source;Destination;Bandwidth;EdgeDelay;EdgeCost\n"
        fp.write(heading)

        for cnt in range(number_of_links):
            src = random.randint(1, number_of_nodes)
            dest = random.randint(1, number_of_nodes)
            bw = random.randint(0, 1000)
            ed = random.randint(0, 1000)
            ec = random.randint(0, 1000)

            linkLine = "{};{};{};{};{}\n".format(src, dest, bw, ed, ec)
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
            requestedBW = 5

            if dest == src:
                dest = random.randint(1, number_of_nodes)

            requested_num_func = random.randint(1, 6)  # Random amount of functions
            outputFunctions = []    # The random list of functions

            i = 1

            for i in range(requested_num_func):
                if i <= requested_num_func:
                    current_func = FuncObj.RANDOM
                    current_func = current_func.name
                    if current_func not in outputFunctions:
                        outputFunctions.append(current_func)
                i += 1

            requestLine = "{};{};{};{};{};\n".format(reqID, src, dest, outputFunctions, requestedBW)
            fp.write(requestLine)


if __name__ == '__main__':
    createNodeInputData(6)
    createLinkInputData(10, 6)
    createRequests(10, 6)
