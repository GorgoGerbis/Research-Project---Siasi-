from src.VNFObj import VNFObj
from src.CONSTANTS import node_resources as GLOBAL_NODE_RESOURCES
from src.CONSTANTS import GLOBAL_REQUEST_DELAY_THRESHOLD
import random

"""
@author: Jackson Walker
"""

# ToDo Need to make a method returning these values so only need to edit VNFObj.py when adding a new function.
FUNCTION_COSTS = [[1, 1, 2], [2, 2, 4], [3, 3, 6], [4, 4, 8], [5, 5, 10]]

# ToDo need to adjust this
REQUEST_DELAY_THRESHOLD = GLOBAL_REQUEST_DELAY_THRESHOLD


class NodeObj:

    AUTO_FAIL = []
    AUTO_FAIL_PATH_TWO = []

    # BE CAREFUL WHEN CHANGING THINGS IN THIS CLASS ITS USED EVERYWHERE
    StaticLinkList = []  # Static List of all links
    StaticNodeList = []  # Static List of all nodes
    TotalNodeCount = 0  # Static variable keeping track of amount of nodes

    StaticNodeResources_PATHONE = []
    StaticNodeResources_PATHTWO = []

    StaticLinkResources_PATHONE = []
    StaticLinkResources_PATHTWO = []

    # NODE STATUS
    UNAVAILABLE = "O"
    AVAILABLE = "A"
    RELAY = "R"

    def __init__(self, nodeID, status, nodeResources, processingDelay, nodeCost, failure_probability):
        self.nodeID = nodeID
        self.status = status
        self.nodeCost = nodeCost
        self.processingDelay = processingDelay
        self.nodeResources = nodeResources
        self.failure_probability = failure_probability

        NodeObj.StaticNodeList.append(self)  # <-- APPENDS CURRENT NODE TO STATIC LIST OF ALL NODES

#################################################################################################

    def can_map(self, vnfObj):  # <---- @ToDo made to replace check_mappable!
        cpu = vnfObj[0]
        ram = vnfObj[1]

        if self.compareCPU(cpu) and self.compareRAM(ram):
            return True
        else:
            return False

    def can_node_map_all_funcs_given(self, vnfs=None):  # <--- Allows me to overload this
        """
        Will return true if all funcs can be mapped at given node at once.
        :param vnfs: optional argument, if not specifying the VNFs to check then simply check all VNF types.
        :return: True if we can map each func given here at once...
        """
        mappable_at_once = []

        cpu = self.nodeResources[0]
        ram = self.nodeResources[1]

        total_req_cpu = 0
        total_req_ram = 0

        if vnfs is None:
            all_possible_vnfs = [e.value for e in VNFObj]
        else:
            all_possible_vnfs = vnfs.copy()

        i = 0

        while True:
            if i >= len(all_possible_vnfs):
                break
            else:
                if not (total_req_cpu <= cpu) or not (total_req_ram <= ram):
                    return False
                else:
                    f = all_possible_vnfs[i]
                    total_req_cpu += f.value[0]
                    total_req_ram += f.value[1]
            i += 1
        return True

    def what_can_node_map_at_once(self, vnfs=None):     # <--- Allows me to overload this
        """
        Will return the VNFs that can all be mapped at once to this particular node.
        :param vnfs: optional argument, if not specifying the VNFs to check then simply check all VNF types.
        :return: List of all VNFs you can map
        """
        mappable_at_once = []

        cpu = self.nodeResources[0]
        ram = self.nodeResources[1]

        total_req_cpu = 0
        total_req_ram = 0

        if vnfs is None:
            all_possible_vnfs = [e.value for e in VNFObj]
        else:
            all_possible_vnfs = vnfs.copy()

        for f in all_possible_vnfs:
            total_req_cpu += f.value[0]
            total_req_ram += f.value[1]
            if (total_req_cpu <= cpu) and (total_req_ram <= ram):
                mappable_at_once.append(f)

        return mappable_at_once

#################################################################################################

    def reset_node(self):
        for pair in NodeObj.StaticNodeResources:
            if self.nodeID == pair[0]:
                self.nodeResources = GLOBAL_NODE_RESOURCES
                self.status = 'A'

    def get_neighbors(self):
        neighbors = []
        for lnk in NodeObj.StaticLinkList:
            if lnk.linkDest == self.nodeID:
                n = self.returnNode(lnk.linkSrc)
                neighbors.append(n)
            elif lnk.linkSrc == self.nodeID:
                n = self.returnNode(lnk.linkDest)
                neighbors.append(n)
        return neighbors

    def check_isolated(self):
        tethers = self.get_tethers()
        count = 0
        for obj in tethers:
            if obj.linkStatus == "O":
                count += 1

        if count == len(tethers):
            return True

    def get_tethers(self):
        output = []
        for link in NodeObj.StaticLinkList:
            if (link.linkDest == self.nodeID) or (link.linkSrc == self.nodeID):
                output.append(link)

        return output

    def compareCPU(self, cpu): # Return True if we have enough resources
        if self.nodeResources[0] >= cpu:
            return True
        else:
            return False

    def compareRAM(self, ram):
        if self.nodeResources[1] >= ram:
            return True
        else:
            return False

    def how_many_functions_mappable(self, func_list):
        mappable_funcs = []
        num_mappable = 0

        t_cpu = 0
        t_ram = 0

        for f in func_list:
            temp_func = VNFObj.retrieve_function_value(f)  # Retrieves the current requested function
            # Current func requirements
            c_cpu = temp_func.value[0] + t_cpu
            c_ram = temp_func.value[1] + t_ram

            if self.HELPER_check_enough_resources(c_cpu, c_ram):
                t_cpu += temp_func.value[0]
                t_ram += temp_func.value[1]
                mappable_funcs.append(temp_func)
                num_mappable += 1
            else:
                return mappable_funcs

        return mappable_funcs

    def map_function(self, cpu, ram):
        self.nodeResources[0] = int(self.nodeResources[0]) - cpu
        self.nodeResources[1] = int(self.nodeResources[1]) - ram

    def map_function_obj(self, f):
        if type(f) == VNFObj:
            func = VNFObj.retrieve_function_value(f)
            self.nodeResources[0] = int(self.nodeResources[0]) - func.value[0]
            self.nodeResources[1] = int(self.nodeResources[1]) - func.value[1]
        else:
            func = f
            self.nodeResources[0] = int(self.nodeResources[0]) - func[0]
            self.nodeResources[1] = int(self.nodeResources[1]) - func[1]

    def check_enough_resources(self, f):
        func = VNFObj.retrieve_function_value(f)
        c, r= func.value[0], func.value[1]
        if self.compareCPU(c) and self.compareRAM(r):
            return True
        else:
            # print("NODE {} DOES NOT HAVE SUFFICIENT RESOURCES TO MAP FUNCTION {}\n".format(self.nodeID, func))
            return False

    def check_region(self, x, y):
        if x[0] <= self.nodeID <= x[1]:
            if y[0] <= self.nodeID <= y[1]:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def calculate_failure(nid):
        """
        calculate whether or not a node has failed.
        :param nid = nodeID
        :return: True if success, False if failed
        """
        n = NodeObj.returnNode(nid)
        number_of_failures = REQUEST_DELAY_THRESHOLD * n.failure_probability
        fail_rate = (number_of_failures + 1) / (REQUEST_DELAY_THRESHOLD + 2)
        return fail_rate

    @staticmethod
    def returnNode(node_id):
        for node in NodeObj.StaticNodeList:
            if node.nodeID == node_id:
                return node

    @staticmethod
    def print_resources(node):
        output = [node.nodeID, node.nodeResources[0], node.nodeResources[1]]
        return output

    def __str__(self):
        string = "Node ID: {} Node Status: {} Node Resources: {} Processing Delay: {} Node cost: {} Failure probability: {}".format(
            self.nodeID, self.status, self.nodeResources, self.processingDelay, self.nodeCost, self.failure_probability)
        return string
