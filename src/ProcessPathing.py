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

# def process_path_resources_node(req, path):
#
#     unmapped_functions = req.requestedFunctions # List of requested functions]
#     count = 0
#
#     while len(unmapped_functions) != 0:
#         for step in path:
#             print(step)
#             for current_node in NodeObj.StaticNodeList:
#                 if current_node.nodeID == step:
#                     step_node = current_node    # Finally get the needed node, this method can be avoided
#             resources = step_node.nodeResources
#             if resources > unmapped_functions.pop(count):


# This basically manages this script - Functions as control panel
# Maybe nake this into its own seperate class.
def run():
    set_graph_nodes()
    set_graph_edges()
    print("SETUP NODES AND EDGES")

    paths = nx.all_simple_paths(GRAPH, "3", "5")
    print(list(paths))

    # Request 7;3;5;['F4', 'F6', 'F2'];5

    nx.draw(GRAPH, with_labels=True, font_weight='bold')
    plt.show()
