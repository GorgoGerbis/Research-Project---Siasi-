# MY OWN CLASSES
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.Request import Request
from src.FuncObj import FuncObj

# Todo Need to come up with a solution that resets the nodes available resources after request has been processed
# ToDo need to find a way to constantly feed the path that is currently being processed on.
# Todo will need to find a way to accurately calculate the physical buffer size


def find_path_one():
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

def dijkstra_shortest_path_with_resources(GRAPH, starting_node, ending_node):
    visited_nodes = []
    unvisited_nodes = STATIC_ALL_NODES

    while(len(unvisited_nodes) > 0):    # While nodes remain unvisited
        visit


if __name__ == '__main__':
    print("<----------------ProcessPathing.py began processing all requests---------------->\n")
    print("<----------------ProcessPathing.py finished processing all requests---------------->\n")
