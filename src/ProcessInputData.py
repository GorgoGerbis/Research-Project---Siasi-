import os
import random
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.RequestObj import RequestObj

from src.CONSTANTS import GLOBAL_REQUEST_DELAY_THRESHOLD

from src.CONSTANTS import NodeInputData
from src.CONSTANTS import LinkInputData
from src.CONSTANTS import RequestInputData

from src.CONSTANTS import GLOBAL_REQUEST_DELAY_THRESHOLD


def processInputDataNode(filePath):
    with open(filePath) as fp:
        fp.readline()  # <-- This is so that it skips the first line
        for cnt, line in enumerate(fp):
            # print("Line {}: {}".format(cnt, line))
            currentElements = line.split(';')

            # This is so the resources are seperated into a list
            temp_resources = currentElements.pop(2)
            temp_resources = temp_resources.strip('][').split(', ')
            resources = list(map(int, temp_resources))

            id = int(currentElements[0])
            status = currentElements[1]
            processingDelay = float(currentElements[2])
            cost = float(currentElements[3])
            failure = float(currentElements[4].strip('\n'))

            # NodeObj.StaticNodeResources.append([id, resources])   # @ToDo remember to change this as well so the nodes are properly reset
            current_node = NodeObj(id, status, resources, processingDelay, cost, failure) # current_node = NodeObj(id, status, node_resources, processingDelay, cost, failure)
            print(current_node)


def processInputDataLink(filePath):
    with open(filePath) as fp:
        fp.readline()  # <-- This is so that it skips the first line
        for cnt, line in enumerate(fp):
            print("Line {}: {}".format(cnt, line))

            currentElements = line.split(';')

            linkID = int(currentElements[0])
            status = "A"
            source = int(currentElements[1])
            destination = int(currentElements[2])
            bandwidth = int(currentElements[3])
            edgeDelay = float(currentElements[4])
            edgeCost = float(currentElements[5])
            failure_probability = float(currentElements[6].strip('\n'))

            # NodeObj.StaticLinkResources.append([linkID, bandwidth])
            current_link = LinkObj(linkID, status, source, destination, bandwidth, edgeDelay, edgeCost, failure_probability)    # current_link = LinkObj(linkID, status, source, destination, bandwidth, edgeDelay, edgeCost, failure_probability)

            if current_link not in NodeObj.StaticLinkList:
                NodeObj.StaticLinkList.append(current_link)


def processInputDataRequests(filePath):
    with open(filePath) as fp:
        fp.readline()  # <-- This is so that it skips the first line
        for cnt, line in enumerate(fp):
            if (line == "\n") or (line == ""):
                continue
            else:
                line = line.strip('\n')
                currentElements = line.split(';')

                tempRequestedFunctions = currentElements.pop(3)
                tempRequestedFunctions = (tempRequestedFunctions.strip('][')).split(', ')
                requestNum = int(currentElements[0])
                srcNode = int(currentElements[1])
                destNode = int(currentElements[2])
                requestedBW = int(currentElements[3])  # .strip('\n')
                requested_failure_threshold = float(currentElements[4])

                request_delay_threshold = GLOBAL_REQUEST_DELAY_THRESHOLD
                request_status = [0, 0]

                requestedFunctions = []
                for i in tempRequestedFunctions:  # This is to get rid of the extra quotes around the functions
                    t = i.strip(" ' ' ")
                    requestedFunctions.append(t)

                current_request = RequestObj(requestNum, srcNode, destNode, requestedFunctions, requestedBW, request_status, GLOBAL_REQUEST_DELAY_THRESHOLD, requested_failure_threshold, None, None)   # current_request = RequestObj(requestNum, srcNode, destNode, requestedFunctions, requestedBW, request_status, request_delay_threshold, None, None)

                RequestObj.STATIC_TOTAL_REQUEST_LIST.append(current_request)
                print("Request: {} has been created.".format(requestNum))

        print("All requests have been created.")


def processAllInputData():
    if os.path.isfile(NodeInputData):
        print("INPUT_DATA_BOT: NODE FILE PATH WORKS!")
        processInputDataNode(NodeInputData)
        print("INPUT_DATA_BOT: NODE DATA FILE PROCESSED NODES CREATED!")
    else:
        print("INPUT_DATA_BOT: COULD NOT OPEN NODE FILE")

    if os.path.isfile(LinkInputData):
        print("INPUT_DATA_BOT: LINK FILE PATH WORKS!")
        processInputDataLink(LinkInputData)
        print("INPUT_DATA_BOT: LINK DATA FILE PROCESSED LINKS CREATED!")
    else:
        print("INPUT_DATA_BOT: COULD NOT OPEN LINK FILE")

    if os.path.isfile(RequestInputData):
        print("INPUT_DATA_BOT: PROCESSING INPUT DATA REQUESTS!")
        processInputDataRequests(RequestInputData)
        print("INPUT_DATA_BOT: FINISHED PROCESSING ALL DATA REQUESTS!")
    else:
        print("INPUT_DATA_BOT: COULD NOT OPEN REQUEST FILE")
