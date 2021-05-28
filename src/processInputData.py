import os
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.Request import Request

# Resources
baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"

resourcesFolder = os.path.join(baseFolder, "resources")
NodeOpt = os.path.join(resourcesFolder, "NodeInputData-EXSMALL-TEST-5-17-21.csv")
LinkOpt = os.path.join(resourcesFolder, "LinkInputData-EXSMALL-TEST-5-17-21.csv")
auto_requests_Opt = os.path.join(resourcesFolder, "requests-EXSMALL-TEST-5-17-21.txt")

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
            resources = currentElements.pop(4)
            resources = resources.strip('][').split(', ')

            id = currentElements[0]
            position = [currentElements[1], currentElements[2]]
            status = currentElements[3]
            processingDelay = currentElements[4]
            cost = currentElements[5].strip('\n')

            newNodeObj = NodeObj(id, position, status, resources, processingDelay, cost)
            print(newNodeObj)


def processInputDataLink(filePath):
    with open(filePath) as fp:
        fp.readline()  # <-- This is so that it skips the first line
        for cnt, line in enumerate(fp):
            print("Line {}: {}".format(cnt, line))

            currentElements = line.split(';')

            linkID = currentElements[0]
            source = currentElements[1]
            destination = currentElements[2]
            bandwidth = currentElements[3]
            edgeDelay = currentElements[4]
            edgeCost = currentElements[5]

            startingNode = NodeObj.returnNode(source)
            endingNode = NodeObj.returnNode(destination)

            # length = calcDistance(startingNode, endingNode)
            length = 1

            current_link = LinkObj(linkID, source, destination, bandwidth, edgeDelay, edgeCost.strip('\n'), length)

            if current_link not in NodeObj.StaticLinkList:
                NodeObj.StaticLinkList.append(current_link)


# def calcDistance(src, dest):
#     if src is not None and dest is not None:
#         x1 = src.nodePosition[0]
#         x2 = dest.nodePosition[0]
#         y1 = src.nodePosition[1]
#         y2 = dest.nodePosition[1]
#
#         a = (int(x1) - int(x2)) ** 2
#         b = (int(y1) - int(y2)) ** 2
#
#         d = (a + b) ** 0.5
#         return d
#     else:
#         return 0


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
                requestNum = currentElements[0]
                srcNode = currentElements[1]
                destNode = currentElements[2]
                requestedBW = currentElements[3]  # .strip('\n')

                requestedFunctions = []
                for i in tempRequestedFunctions:  # This is to get rid of the extra quotes around the functions
                    t = i.strip(" ' ' ")
                    requestedFunctions.append(t)

                r = Request(requestNum, srcNode, destNode, requestedFunctions, requestedBW, 0)

                Request.StaticTotalRequestList.append(r)
                print("Request: {} has been created.".format(requestNum))

        print("All requests have been created.")


def processAllInputData():
    if os.path.isfile(NodeOpt):
        print("NODE FILE PATH WORKS!")
        processInputDataNode(NodeOpt)
        print("NODE DATA FILE PROCESSED NODES CREATED!")
    else:
        print("COULD NOT OPEN NODE FILE")

    if os.path.isfile(LinkOpt):
        print("LINK FILE PATH WORKS!")
        processInputDataLink(LinkOpt)
        print("LINK DATA FILE PROCESSED LINKS CREATED!")
    else:
        print("COULD NOT OPEN LINK FILE")

    if os.path.isfile(auto_requests_Opt):
        print("PROCESSING INPUT DATA REQUESTS!")
        processInputDataRequests(auto_requests_Opt)
        print("FINISHED PROCESSING ALL DATA REQUESTS!")
    else:
        print("COULD NOT OPEN REQUEST FILE")
