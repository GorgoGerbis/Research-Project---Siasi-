import os
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.Request import Request
from src.HvWProtocol import REQUEST_DELAY_THRESHOLD

# Resources
baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
NodeInputData = os.path.join(resourcesFolder, "NodeInputData-EXSMALL-TEST-7-19-21.csv")
LinkInputData = os.path.join(resourcesFolder, "LinkInputData-EXSMALL-TEST-7-19-21.csv")
auto_requests_Opt = os.path.join(resourcesFolder, "requests-EXSMALL-TEST-7-19-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-TEST-A-7-19-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-TEST-A-7-19-21.csv")
# auto_requests_Opt = os.path.join(resourcesFolder, "requests-TEST-A-7-19-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-TEST-B-7-19-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-TEST-B-7-19-21.csv")
# auto_requests_Opt = os.path.join(resourcesFolder, "requests-TEST-B-7-19-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-TEST-C-7-19-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-TEST-C-7-19-21.csv")
# auto_requests_Opt = os.path.join(resourcesFolder, "requests-TEST-C-7-19-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-TEST-D-7-19-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-TEST-D-7-19-21.csv")
# auto_requests_Opt = os.path.join(resourcesFolder, "requests-TEST-D-7-19-21.txt")

REQUESTS_FAILED = []
REQUESTS_PASSED = []
REQUESTS = []


def processInputDataNode(filePath):
    with open(filePath) as fp:
        fp.readline()  # <-- This is so that it skips the first line
        for cnt, line in enumerate(fp):
            # print("Line {}: {}".format(cnt, line))
            currentElements = line.split(';')

            # This is so the resources are seperated into a list
            temp_resources = currentElements.pop(4)
            temp_resources = temp_resources.strip('][').split(', ')
            resources = []

            for i in temp_resources:
                resources.append(int(i))

            id = int(currentElements[0])
            position = [int(currentElements[1]), int(currentElements[2])]
            status = currentElements[3]
            processingDelay = int(currentElements[4])
            cost = int(currentElements[5])

            failure = float(currentElements[6].strip('\n'))

            NodeObj.StaticNodeResources.append([id, [100, 100, 100]])   # @ToDo remember to change this as well so the nodes are properly reset
            current_node = NodeObj(id, position, status, resources, processingDelay, cost, failure)
            print(current_node)


def processInputDataLink(filePath):
    with open(filePath) as fp:
        fp.readline()  # <-- This is so that it skips the first line
        for cnt, line in enumerate(fp):
            print("Line {}: {}".format(cnt, line))

            currentElements = line.split(';')

            linkID = int(currentElements[0])
            source = int(currentElements[1])
            destination = int(currentElements[2])
            bandwidth = int(currentElements[3])
            edgeDelay = float(currentElements[4])
            edgeCost = int(currentElements[5])
            failure_probability = float(currentElements[6].strip('\n'))

            NodeObj.StaticLinkResources.append([linkID, bandwidth])
            current_link = LinkObj(linkID, source, destination, bandwidth, edgeDelay, edgeCost, failure_probability)

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

                request_delay_threshold = REQUEST_DELAY_THRESHOLD
                request_status = [0, 0]

                requestedFunctions = []
                for i in tempRequestedFunctions:  # This is to get rid of the extra quotes around the functions
                    t = i.strip(" ' ' ")
                    requestedFunctions.append(t)

                current_request = Request(requestNum, srcNode, destNode, requestedFunctions, requestedBW, request_status, request_delay_threshold, None, None)

                Request.STATIC_TOTAL_REQUEST_LIST.append(current_request)
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

    if os.path.isfile(auto_requests_Opt):
        print("INPUT_DATA_BOT: PROCESSING INPUT DATA REQUESTS!")
        processInputDataRequests(auto_requests_Opt)
        print("INPUT_DATA_BOT: FINISHED PROCESSING ALL DATA REQUESTS!")
    else:
        print("INPUT_DATA_BOT: COULD NOT OPEN REQUEST FILE")
