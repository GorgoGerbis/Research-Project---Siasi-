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
class pathFinder():


    def __init__(self, pathFinderID, request, src, dest, request_delay, request_delay_threshold, status):
        self.pathFinderID = pathFinderID
        self.request = request
        self.src = src
        self.dest = dest
        self.request_delay = request_delay
        self.request_delay_threshold = request_delay_threshold
        self.status = status