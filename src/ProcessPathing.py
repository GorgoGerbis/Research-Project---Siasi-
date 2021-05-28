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


dfs_visited = set()  # Set to keep track of visited nodes.


def depth_first_search_traversable(visited, graph, node):
    if node not in visited:
        print(node)
        visited.add(node)
        for neighbour in graph[node]:
            depth_first_search_traversable(visited, graph, neighbour)


def run():
    set_graph_nodes()
    set_graph_edges()
    print("SETUP NODES AND EDGES")

    paths = nx.all_simple_paths(GRAPH, "1", "4")
    print(list(paths))

    nx.draw(GRAPH, with_labels=True, font_weight='bold')
    plt.show()
