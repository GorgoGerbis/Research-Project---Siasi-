from src.VNFObj import VNFObj
from src.CONSTANTS import GLOBAL_NODE_RESOURCES, INITIAL_TERMINAL_RESOURCES
from src.CONSTANTS import GLOBAL_REQUEST_DELAY_THRESHOLD
import random

"""
@author: Jackson Walker
"""

# ToDo Need to make a method returning these values so only need to edit VNFObj.py when adding a new function.
FUNCTION_COSTS = [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4], [5, 5, 5], [6, 6, 6]]

# ToDo need to adjust this
NODE_RESOURCES = GLOBAL_NODE_RESOURCES
REQUEST_DELAY_THRESHOLD = GLOBAL_REQUEST_DELAY_THRESHOLD


class TerminalObj:

    def __init__(self, ID, status, resources, PD, cost, fail):
        self.ID = ID
        self.status = status
        self.resources = resources
        self.PD = PD
        self.cost = cost
        self.fail = fail

    def reset(self):  # Reset terminal resources
        self.resources = INITIAL_TERMINAL_RESOURCES

    def get_neighbors(self):
        neighbors = []
        # Return list of nodes I am attached to
        return

    # def get_status(self):  # ToDo need to figure out when and how often the status of a node is checked
    #     if self.check_isolated():
    #         self.status = "O"
    #         NodeObj.AUTO_FAIL.append(self.nodeID)
    #     elif self.check_mappable():
    #         self.status = "A"
    #     else:
    #         self.status = "R"

    # def check_isolated(self):
    #     tethers = self.get_tethers()
    #     count = 0
    #     for obj in tethers:
    #         if obj.linkStatus == "O":
    #             couen(tethers):
    #         return Trnt += 1
    #
    #     if count == lue

    # def map_function(self, cpu, ram, bw):
    #     self.nodeResources[0] = int(self.nodeResources[0]) - cpu
    #     self.nodeResources[1] = int(self.nodeResources[1]) - ram
    #     self.nodeResources[2] = int(self.nodeResources[2]) - bw

    # def map_function_obj(self, f):
    #     # func = FuncObj.retrieve_function_value(f)
    #     if type(f) != FuncObj:
    #         func = FuncObj.retrieve_function_value(f)
    #     else:
    #         func = f

    #     self.nodeResources[0] = int(self.nodeResources[0]) - func.value[0]
    #     self.nodeResources[1] = int(self.nodeResources[1]) - func.value[1]
    #     self.nodeResources[2] = int(self.nodeResources[2]) - func.value[2]

    def __str__(self):
        return "Terminal ID: {}, Status: {}, Resources {}, Processing Delay: {}, Cost {}, Failure probability {}".format(
            self.ID, self.status, self.resources, self.PD, self.cost, self.fail)
