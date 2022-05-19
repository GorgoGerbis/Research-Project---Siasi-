"""
Setup Script
author: Jackson Walker

Similar to an observer class/design method. Will trigger when to start and stop doing something.

1. Responsible for notifying when events are triggered/completed.
2. Needs to update the resource utilization of nodes, terminals and links.
"""
# Need these for path finding and graphing
import networkx as nx
import matplotlib.pyplot as plt

from src.NodeObj import NodeObj
from src.Request import Request
from src.PathObj import PathObj

def update_all(msg):    # @ToDo need to implement
    """
    Notifies/updates all components/objects in the hierarchy of events and triggers.
    :param msg: Messsage to broadcast to all
    :return: n/a
    """
    return