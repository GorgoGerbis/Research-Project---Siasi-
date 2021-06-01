import os
from src.NodeObj import NodeObj
from src.Request import Request
from src.Graph_Class import Graph
from src import processInputData

# ProcessPathing
from src import ProcessPathing, outputData

REQUESTS_FAILED = []
REQUESTS_PASSED = []
REQUESTS = []

# Need these for path finding
GRAPH = Graph()
edges = []


def processFailureProbablity():
    for node in NodeObj.StaticNodeList:
        if int(node.failureProbablity) >= 3:
            node.status == "R"
        else:
            node.status == "A"


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


def set_edges():
    visited_links = []

    for link in NodeObj.StaticLinkList:
        current_link_tup = (link.linkSrc, link.linkDest, link.linkWeight)
        if current_link_tup not in visited_links:
            edges.append(current_link_tup)
            visited_links.append(visited_links)


def dijsktra(graph, start, end):
    # shortest paths is a dict of nodes
    # whose values is a tuple of (previous node, weight)
    shortest_paths = {start: (None, 0)}
    current_node = start
    visited = set()  # <-- what does set() do?

    weight = 0  # Defining this variable early
    count = 0

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            # weight += graph.weights[(current_node, next_node)] + weight_to_current_node
            count += 1
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


# def processData():
#     processInputData.processAllInputData()
#     print("Input data processed!")
#
#     set_edges()
#
#     for edge in edges:
#         GRAPH.add_edge(*edge)
#
#     print("Processing requests")
#     for req in Request.StaticTotalRequestList:
#         processRequest(req)
#     print("ALL REQUESTS PROCESSED")
#
#     outputData.create_output(REQUESTS, REQUESTS_FAILED, REQUESTS_PASSED)
#     print("FINISHED!")

if __name__ == '__main__':
    processInputData.processAllInputData()
    print("Input data processed!")

    processFailureProbablity()
    ProcessPathing.run()
