# MY OWN CLASSES
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.Request import Request
from src.FuncObj import FuncObj
# from src.ProcessPathing import
# Need these for path finding
import networkx as nx
import matplotlib.pyplot as plt
from itertools import islice

"""
Note that the overall delay in the path does not include the trials of alternative (candidate) nodes. 
The path delay includes only the delay traversing over the host (selected) nodes and links. Only the final choices. 
"""


class pathFinder():

    def __init__(self, path_finder_ID, request, path_one, path_two, request_delay, request_delay_threshold, status,
                 STATE):
        self.path_finder_ID = path_finder_ID
        self.request = request
        self.path_one = path_one
        self.path_two = path_two
        self.request_delay = request_delay
        self.request_delay_threshold = request_delay_threshold
        self.status = status

        self.STATE = self.check_failed()

    def check_failed(self):
        if self.request_delay > self.request_delay_threshold:
            return False
        # if request.resources == enough
        # return False
        # if request.traversable == not
        # return False
        # if request.

    def __str__(self):
        return "Request: {} PathFinder: {} Status: {}\n".format(self.request, self.path_finder_ID, self.status)
