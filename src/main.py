import os

from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.Request import Request
from src.Function import Function

# For path finding
# Link for this function --> "https://networkx.org/documentation/networkx-1.10/_modules/networkx/algorithms/simple_paths.html#shortest_simple_paths"
from itertools import islice
import networkx as nx

# Other option
# https://www.geeksforgeeks.org/check-if-a-directed-graph-is-connected-or-not/

# Resources
baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
LinkOpt = os.path.join(resourcesFolder, "LinkOpt.csv")
NodeOpt = os.path.join(resourcesFolder, "NodeOpt.csv")
auto_requests_Opt = os.path.join(resourcesFolder, "auto_requests_Opt.txt")

# My new data I created
NodeInputData = os.path.join(resourcesFolder, "NodeInputData.csv")

TEMPNODE = []
TEMPLINK = []


def processRequest(req):
    print("<----- Processing Request Number: {}\nSource: {}\nDestination: {}\n".format(req.requestID, req.source, req.destination))
    SourceID = 0
    DestID = 0

    for node in NodeObj.StaticNodeList:
        if node.nodeID == req.source:
            SourceID = req.source
            break

    for node in NodeObj.StaticNodeList:
        if node.nodeID == req.destination:
            DestID = req.destination

    # output = find_path(NodeObj.StaticLinkList, SourceID, DestID)
    # print("Request number {} path {}".format(req.requestID, output))
    # return output


def createFunctions():
    functionOne = Function("f1", 10, 10, 10)
    functionTwo = Function("f2", 5, 5, 5)
    functionThree = Function("f3", 30, 30, 30)
    functionFour = Function("f4", 35, 35, 35)
    functionFive = Function("f5", 1, 1, 1)

    print("Created functions: {}, {}, {}, {}, {}".format(functionOne.functionID, functionTwo.functionID,
                                                         functionThree.functionID, functionFour.functionID,
                                                         functionFive.functionID))


def processInputDataRequests(filePath):
    with open(filePath) as fp:
        fp.readline()  # <-- This is so that it skips the first line
        for cnt, line in enumerate(fp):
            if (line == "\n") or (line == ""):
                continue
            else:
                line = line.strip('\n')
                currentElements = line.split(';')

                requestedFunctions = ((currentElements.pop(3)).strip('['))
                requestedFunctions = (requestedFunctions.strip(']')).split(',')
                requestNum = currentElements[0]
                srcNode = currentElements[1]
                destNode = currentElements[2]
                requestedBW = currentElements[3]  # .strip('\n')

                r = Request(requestNum, srcNode, destNode, requestedFunctions, requestedBW, 0)
                Request.StaticTotalRequestList.append(r)
                print("Request: {} has been created.".format(requestNum))

        print("All requests have been created.")


def fillConnectedLinks():
    for n in NodeObj.StaticNodeList:
        for l in NodeObj.StaticLinkList:
            if l.linkSrc == n.nodeID:
                n.addLinksToNetwork(l)
        n.printConnectedLinks()

    print("CREATED LIST OF CONNECTED LINKS FOR EACH NODE!")

    # Provides List of all links for this node
    def createConnectedNodesList(self):
        for obj in NodeObj.StaticLinkList:
            if self.id == obj.showLinkSourceId():
                self.connectedLinks.append(obj)

        return self.connectedLinks


def processInputDataNode(filePath):
    with open(filePath) as fp:
        fp.readline()  # <-- This is so that it skips the first line
        for cnt, line in enumerate(fp):
            # print("Line {}: {}".format(cnt, line))
            currentElements = line.split(';')

            resources = currentElements.pop(4)
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

            source = currentElements[0]
            destination = currentElements[1]
            bandwidth = currentElements[2]
            edgeDelay = currentElements[3]
            edgeCost = currentElements[4]

            LinkObj(source, destination, bandwidth, edgeDelay, edgeCost.strip('\n'))


def processData():
    processInputDataRequests(auto_requests_Opt)
    createFunctions()  # <---- Creates all functions

    if os.path.isfile(NodeInputData):
        print("NODE FILE PATH WORKS!")
        processInputDataNode(NodeInputData)
        print("NODE DATA FILE PROCESSED NODES CREATED!")

    if os.path.isfile(LinkOpt):
        print("LINK FILE PATH WORKS!")
        processInputDataLink(LinkOpt)
        print("LINK DATA FILE PROCESSED LINKS CREATED!")

    if os.path.isfile(auto_requests_Opt):
        print("PROCESSING INPUT DATA REQUESTS!")
        processInputDataRequests(auto_requests_Opt)
        print("FINISHED PROCESSING ALL DATA REQUESTS!")

    for obj in NodeObj.StaticLinkList:
        print(obj)
        print("-----------")

    heyMan = processGraphData()
    print(heyMan)

    print("FINISHED!")


def processGraphData():
# the purpose of this method is to create a graph of all links and their corresponding siblings
    nodes = []
    node_dict = {}

    for link in NodeObj.StaticLinkList:
        count = 0
        node_links = []
        currentID = link.linkSrc

        # Checks if the node ID has already been accounted for
        if link.linkSrc not in nodes:
            nodes.append(link.linkSrc)

        # Iterates through the list of links finding every single neighbor for currentID
        for l in NodeObj.StaticLinkList:
            if l.linkSrc == currentID:
                count += 1
                node_links.append(l.linkDest)

        node_dict.setdefault(currentID, node_links)

    return node_dict