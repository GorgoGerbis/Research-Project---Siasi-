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

GRAPH = nx.Graph()
edges = []

POSSIBLE_PATHS = []


def set_graph_nodes():
    added_nodes = []
    for node in NodeObj.StaticNodeList:
        if node not in added_nodes:
            added_nodes.append(node)
            GRAPH.add_node(node.nodeID)


def set_graph_edges():
    visited_links = []
    for link in NodeObj.StaticLinkList:
        if link not in visited_links:
            GRAPH.add_edge(link.linkSrc, link.linkDest)
            visited_links.append(link)


def get_current_link(src, dest):
    for link in NodeObj.StaticLinkList:
        if link.linkSrc == src and link.linkDest == dest:
            return link


def get_current_node(id):
    for node in NodeObj.StaticNodeList:
        if node.nodeID == id:
            return node


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


# ToDo Process if a path has enough resources to be traversed
# ToDo Have to update the network if resources have been taken so that next path doesnt use unavailable resources
# def process_path_resources(req, path):
#     unmapped_functions = req.requestedFunctions
#     while len(unmapped_functions > 0):
#         for step in path:
#             if can_map == True:
#                 map_func(func)
#                 unmapped_functions.pop(func)
#                 # go to next step
#             else if num_func <= num_nodes_left:
#                 if can_traverse_forward:
#                     skip_current_node
#                     # go to next step
#             else:
#                 raise not_enough_resources
#     return

def process_path_resources_node(req, path):
    unmapped_functions = req.requestedFunctions  # List of requested functions
    count = 0

    while count < len(unmapped_functions):  # while they're still functions that have yet to be mapped
        for step in path:
            for current_node in NodeObj.StaticNodeList:
                if current_node.nodeID == step:
                    step_node = current_node  # Finally get the needed node, this method can be avoided
                    if count >= len(unmapped_functions):
                        break
                    current_func = FuncObj.__getattr__(unmapped_functions[count])  # Will always get the next function up
                    if step_node.compareCPU(current_func.value[0]) and step_node.compareRAM(current_func.value[1]) and step_node.compareBW(current_func.value[2]):  # Checks to see if this node has enough resources to map the func
                        print("NODE HAS ENOUGH RESOURCES TO MAP FUNCTION {}".format(current_func))
                        count += 1
                    else:
                        print("NODE DOES NOT HAVE ENOUGH RESOURCES")


"""
@ process_resources_node(func, node)
Smaller helper function that basically does what process_path_resources
does but only for a particular node and a particular request.
"""


def process_resources_node(func, node):
    current_func = FuncObj.__getattr__(func)
    if node.compareCPU(current_func.value[0]) and node.compareRAM(current_func.value[1]) and node.compareBW(
            current_func.value[2]):  # Checks to see if this node has enough resources to map the func
        node.map_function(current_func.value[0], current_func.value[1], current_func.value[2])
        return True
    else:
        return False


"""
@ process_resources_link(req, link)
Smaller helper function that processes if link has enough resources to be used.
"""


def process_resources_link(req, link):
    if link.compareBW(req.requestedBW):
        link.map_request(req.requestedBW)
        return True
    else:
        return False


# This basically manages this script - Functions as control panel
# Maybe nake this into its own seperate class.
def run():
    set_graph_nodes()
    set_graph_edges()
    print("SETUP NODES AND EDGES")  # setup the graph

    # paths = nx.all_simple_paths(GRAPH, "17", "19")
    # print(list(paths))

    # shortest_path = nx.shortest_path(GRAPH, "17", "19")
    # print("<---------- SHORTEST PATH {} --------------->".format(shortest_path))

    # Request 1;17;19;['F4', 'F6'];5
    # path = ['17', '2', '23', '19']
    # req = Request(1, '17', '19', ['F4', 'F6'], 5, 0)
    # process_path_resources_node(req, path)

    print("<----------------ProcessPathing.py began processing all requests---------------->\n")
    for req in Request.StaticTotalRequestList:
        shortest_path = nx.shortest_path(GRAPH, req.source, req.destination)
        print("Request: {} Shortest Path: {}\n".format(req.requestID, shortest_path))
        process_path_resources_node(req, shortest_path)


    nx.draw(GRAPH, with_labels=True, font_weight='bold')
    plt.show()