# MY OWN CLASSES
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.Request import Request
from src.FuncObj import FuncObj


# Todo Need to come up with a solution that resets the nodes available resources after request has been processed
# ToDo need to find a way to constantly feed the path that is currently being processed on.
# Todo will need to find a way to accurately calculate the physical buffer size

def create_adjacency_list():
    adjacency_list = []

def set_edges():
    visited_links = []

    for link in NodeObj.StaticLinkList:
        current_link_tup = (link.linkSrc, link.linkDest, link.linkWeight)
        if current_link_tup not in visited_links:
            edges.append(current_link_tup)
            visited_links.append(visited_links)

def breadth_first_search_traversable():
    return