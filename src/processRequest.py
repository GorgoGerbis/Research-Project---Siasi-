# MY OWN CLASSES
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.Request import Request
from src.FuncObj import FuncObj

# Todo Need to come up with a solution that resets the nodes available resources after request has been processed
# ToDo need to find a way to constantly feed the path that is currently being processed on.
# Todo will need to find a way to accurately calculate the physical buffer size

# Need these for path finding
import networkx as nx
import matplotlib.pyplot as plt
from itertools import islice

def dijsktra_mod(graph, start, end):
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

def find_path_one(req):
    """
    WITHOUT FAILURE PROBABILITY

    The goal of this method is to return the first path. This path is
    the shortest traversable path from src to dest WITHOUT calculating
    failure probability.

    Both of these functions calculate the resources being used

    :return: path_one : a list of the nodes showing the current path.
    """
    return


def find_path_two():
    """
    WITH FAILURE PROBABILITY

    The goal of this method is to return the second path. This path is
    the shortest traversable path from src to dest that CALCULATES
    failure probability.

    Both of these functions calculate the resrouces being used.

    :return: path_one : a list of the nodes showing the current path.
    """
    return

if __name__ == '__main__':

    print("<----------------ProcessPathing.py began processing all requests---------------->\n")
    for req in Request.StaticTotalRequestList:
        path_one = dijsktra_mod(GRAPH, 1, 18)
    print("<----------------ProcessPathing.py finished processing all requests---------------->\n")