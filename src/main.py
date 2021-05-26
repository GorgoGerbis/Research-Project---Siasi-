import os

from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.Request import Request
from src.FuncObj import FuncObj
from src.Graph_Class import Graph

# ProcessPathing
from src import ProcessPathing, outputData

# Resources
baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"

resourcesFolder = os.path.join(baseFolder, "resources")
NodeOpt = os.path.join(resourcesFolder, "NodeInputData-EXSMALL-TEST-5-17-21.csv")
LinkOpt = os.path.join(resourcesFolder, "LinkInputData-EXSMALL-TEST-5-17-21.csv")
auto_requests_Opt = os.path.join(resourcesFolder, "requests-EXSMALL-TEST-5-17-21.txt")

REQUESTS_FAILED = []
REQUESTS_PASSED = []
REQUESTS = []

# Need these for path finding
GRAPH = Graph()
edges = []


def processRequest(req):
    print("<----- Processing Request Number: {} Source: {} Destination: {}".format(req.requestID, req.source,
                                                                                   req.destination))
    output_Dijkstra = dijsktra(GRAPH, req.source, req.destination)

    output_list = [req.requestID, req.source, req.destination, req.requestedFunctions, req.requestedBW, output_Dijkstra]
    print("Request ID: {} {}\n".format(req.requestID, output_Dijkstra))

    REQUESTS.append(output_list)

    if "Route Not Possible" in output_list:
        REQUESTS_FAILED.append(output_list)
    else:
        REQUESTS_PASSED.append(output_list)

    print("ALL REQUESTS PROCESSED")


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

            length = calcDistance(startingNode, endingNode)

            current_link = LinkObj(linkID, source, destination, bandwidth, edgeDelay, edgeCost.strip('\n'), length)
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

    weight = 0  # Defining this variable early

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight += graph.weights[(current_node, next_node)] + weight_to_current_node
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


def processData():
    processAllInputData()
    print("Input data processed!")

    r, n, l = ProcessPathing.find_specific_data("1", "1", "1")
    ProcessPathing.calculate_path(r, n, l)

    set_edges()

    for edge in edges:
        GRAPH.add_edge(*edge)

    print("Processing requests")
    for req in Request.StaticTotalRequestList:
        processRequest(req)

    outputData.create_output(REQUESTS, REQUESTS_FAILED, REQUESTS_PASSED)
    print("FINISHED!")

# if __name__ == '__main__':
#     processAllInputData()
#     print("Input data processed!")
#
#     set_edges()
#
#     for edge in edges:
#         GRAPH.add_edge(*edge)
#
#     for req in Request.StaticTotalRequestList:
#         processRequest(req)
#
#     print("FINISHED!")
