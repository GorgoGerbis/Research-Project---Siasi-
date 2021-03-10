import os
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.Request import Request
from src.Function import Function

from src.Pathfinder import Pathfinder

# Resources
baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
LinkOpt = os.path.join(resourcesFolder, "LinkOpt.csv")
NodeOpt = os.path.join(resourcesFolder, "NodeOpt.csv")
auto_requests_Opt = os.path.join(resourcesFolder, "auto_requests_Opt.txt")


def createFunctions():
    functionOne = Function("f1", 10, 10, 10)
    functionTwo = Function("f2", 5, 5, 5)
    functionThree = Function("f3", 30, 30, 30)
    functionFour = Function("f4", 35, 35, 35)
    functionFive = Function("f5", 1, 1, 1)

    print("Created functions: {}, {}, {}, {}, {}".format(functionOne.functionID, functionTwo.functionID, functionThree.functionID, functionFour.functionID, functionFive.functionID))

def findNodeSiblings(nodeObj):
    for link in NodeObj.StaticLinkList:
        if link.linkDest == nodeObj.nodeID:
            nodeObj.siblingLinks.append(link)

    for link in nodeObj.siblingLinks:
        current_link = link.linkSrc
        for node in NodeObj.StaticNodeList:
            if node.nodeID == current_link:
                nodeObj.siblingNodes.append(node.nodeID)

def processInputDataRequests(filePath):
    with open(filePath) as fp:
        fp.readline()   # <-- This is so that it skips the first line
        for cnt, line in enumerate(fp):
            if (line == "\n") or (line != ""):
                break
            else:
                line = line.strip('\n')
                currentElements = line.split(';')

                requestedFunctions = ((currentElements.pop(3)).strip('['))
                requestedFunctions = (requestedFunctions.strip(']')).split(',')
                requestNum = currentElements[0]
                srcNode = currentElements[1]
                destNode = currentElements[2]
                requestedBW = currentElements[3]  # .strip('\n')

                newRequest = Request(requestNum, srcNode, destNode, requestedFunctions, requestedBW, 0)
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


if __name__ == '__main__':

    processInputDataRequests(auto_requests_Opt)
    createFunctions()   # <---- Creates all functions




    if os.path.isfile(NodeOpt):
        print("NODE FILE PATH WORKS!")
        processInputDataNode(NodeOpt)
        print("NODE DATA FILE PROCESSED NODES CREATED!")

        if os.path.isfile(LinkOpt):
            print("LINK FILE PATH WORKS!")
            processInputDataLink(LinkOpt)
            print("LINK DATA FILE PROCESSED LINKS CREATED!")

        for obj in NodeObj.StaticLinkList:
            print(obj)
            print("-----------")

        fillConnectedLinks()

        for node in NodeObj.StaticNodeList:
            findNodeSiblings(node)
            print("Node: {} Siblings: {}".format(node.nodeID, node.siblingNodes))

        print("FINISHED!")

    else:
        print("THIS PATH DOES NOT WORK!")
