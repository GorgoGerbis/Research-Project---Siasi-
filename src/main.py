import os

from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.Request import Request
from src.Function import Function
from src.Graph_Class import Graph


# Resources
baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
LinkOpt = os.path.join(resourcesFolder, "LinkInputData.csv")
NodeOpt = os.path.join(resourcesFolder, "NodeInputData.csv")
auto_requests_Opt = os.path.join(resourcesFolder, "auto_requests_Opt.txt")

# My new data I created
NodeInputData = os.path.join(resourcesFolder, "NodeInputData.csv")

# Need these for path finding
GRAPH = Graph()
edges = []


def processRequest(req):
    print("<----- Processing Request Number: {} Source: {} Destination: {}".format(req.requestID, req.source, req.destination))
    output = dijsktra(GRAPH, req.source, req.destination)
    print("{}\n".format(output))


def createFunctions():
    functionOne = Function("f1", 10, 10, 10)
    functionTwo = Function("f2", 5, 5, 5)
    functionThree = Function("f3", 30, 30, 30)
    functionFour = Function("f4", 35, 35, 35)
    functionFive = Function("f5", 1, 1, 1)

    print("Created functions: {}, {}, {}, {}, {}".format(functionOne.functionID, functionTwo.functionID,
                                                         functionThree.functionID, functionFour.functionID,
                                                         functionFive.functionID))


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

            startingNode = NodeObj.returnNode(source)
            endingNode = NodeObj.returnNode(destination)

            length = calcDistance(startingNode, endingNode)

            current_link = LinkObj(source, destination, bandwidth, edgeDelay, edgeCost.strip('\n'), length)
            NodeObj.StaticLinkList.append(current_link)


def calcDistance(src, dest):
    if src is not None and dest is not None:
        x1 = src.nodePosition[0]
        x2 = dest.nodePosition[0]
        y1 = src.nodePosition[1]
        y2 = dest.nodePosition[1]

        a = (int(x1) - int(x2)) ** 2
        b = (int(y1) - int(y2)) ** 2

        d = (a + b) ** 0.5
        return d
    else:
        return 0


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


def processAllInputData():
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


def set_edges():
    visited_links = []

    for link in NodeObj.StaticLinkList:
        current_link_tup = (link.linkSrc, link.linkDest, link.linkWeight)
        if current_link_tup not in visited_links:
            edges.append(current_link_tup)
            visited_links.append(visited_links)


def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose values is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()  # <-- what does set() do?

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}

        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node

    # Reverse path
    path = path[::-1]
    return "Path: {} Weight: {}".format(path, weight)


# def create_list_of_links_to_draw():
#     for link in NodeObj.StaticLinkList:
#         startingNode = NodeObj.returnNode(link.linkSrc)
#         endingNode = NodeObj.returnNode(link.linkDest)
#
#         starting_node_position = startingNode.nodePosition
#         ending_node_position = endingNode.nodePosition
#


def processData():
# if __name__ == '__main__':
    processAllInputData()
    print("Input data processed!")

    set_edges()

    for edge in edges:
        GRAPH.add_edge(*edge)

    for req in Request.StaticTotalRequestList:
        processRequest(req)

    print("FINISHED!")
