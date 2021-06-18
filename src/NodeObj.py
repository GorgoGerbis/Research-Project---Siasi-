from src.FuncObj import FuncObj
import random
"""
@author: Jackson Walker
"""

# ToDo Need to make a method returning these values so only need to edit FuncObj.py when adding a new function.
FUNCTION_COSTS = [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4], [5, 5, 5], [6, 6, 6]]

class NodeObj:
    # BE CAREFUL WHEN CHANGING THINGS IN THIS CLASS ITS USED EVERYWHERE
    StaticLinkList = []  # Static List of all links
    StaticNodeList = []  # Static List of all nodes
    TotalNodeCount = 0  # Static variable keeping track of amount of nodes

    # NODE STATUS
    UNAVAILABLE = "O"
    AVAILABLE = "A"
    RELAY = "R"

    def __init__(self, nodeID, nodePosition, status, nodeResources, processingDelay, nodeCost, failure_probability):
        self.nodeID = nodeID
        self.nodePosition = nodePosition
        self.status = status
        self.nodeCost = nodeCost
        self.processingDelay = processingDelay
        self.nodeResources = nodeResources
        self.failure_probability = failure_probability

        NodeObj.StaticNodeList.append(self)  # <-- APPENDS CURRENT NODE TO STATIC LIST OF ALL NODES

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

    def get_status(self): # ToDo need to figure out when and how often the status of a node is checked
        if self.check_isolated():
            self.status = "O"
        elif self.check_mappable():
            self.status = "A"
        else:
            self.status = "R"

    def check_isolated(self):
        neighbors = []
        for lnk in NodeObj.StaticLinkList:
            if lnk.linkDest == self.nodeID:
                n = self.returnNode(lnk.linkSrc)
                neighbors.append(n)
            elif lnk.linkSrc == self.nodeID:
                n = self.returnNode(lnk.linkDest)
                neighbors.append(n)

        if len(neighbors) <= 0:
            return True
        else:
            return False

    def compareCPU(self, cpu):
        # Returns True if you have enough resources
        if self.nodeResources[0] >= cpu:
            # print("{} >= {}".format(self.nodeResources[0], cpu))
            return True
        else:
            return False

    def compareRAM(self, ram):
        if self.nodeResources[1] >= ram:
            # print("{} >= {}".format(self.nodeResources[1], ram))
            return True
        else:
            return False

    def compareBW(self, bw):
        if self.nodeResources[2] >= bw:
            # print("{} >= {}".format(self.nodeResources[2], bw))
            return True
        else:
            return False

    def how_many_functions_mappable(self, func_list):
        mappable_funcs = []

        t_cpu = 0
        t_ram = 0
        t_bw = 0

        for f in func_list:
            temp_func = FuncObj.retrieve_function_value(f)  # Retrieves the current requested function
            # Current func requirements
            c_cpu = temp_func.value[0] + t_cpu
            c_ram = temp_func.value[1] + t_ram
            c_bw = temp_func.value[2] + t_bw

            if self.HELPER_check_enough_resources(c_cpu, c_ram, c_bw):
                t_cpu += temp_func.value[0]
                t_ram += temp_func.value[1]
                t_bw += temp_func.value[2]
                mappable_funcs.append(temp_func)
            else:
                return mappable_funcs

        return mappable_funcs

    def map_function(self, cpu, ram, bw):
        self.nodeResources[0] = int(self.nodeResources[0]) - cpu
        self.nodeResources[1] = int(self.nodeResources[1]) - ram
        self.nodeResources[2] = int(self.nodeResources[2]) - bw

    def map_function_obj(self, func):
        self.nodeResources[0] = int(self.nodeResources[0]) - func.value[0]
        self.nodeResources[1] = int(self.nodeResources[1]) - func.value[1]
        self.nodeResources[2] = int(self.nodeResources[2]) - func.value[2]

    def HELPER_check_enough_resources(self, c, r, b):
        if self.compareCPU(c) and self.compareRAM(r) and self.compareBW(b):
            # self.map_function(c, r, b) #ToDo <----DONT FORGET TO COMMENT THIS LINE OUT OR EVERYTHING IS GOING TO BE MAPPED.
            # print("NODE {} DOES HAVE SUFFICIENT RESOURCES TO MAP FUNCTION {}\n".format(self.nodeID, func))
            return True
        else:
            # print("NODE {} DOES NOT HAVE SUFFICIENT RESOURCES TO MAP FUNCTION {}\n".format(self.nodeID, func))
            return False

    def check_enough_resources(self, func):
        c, r, b = func.value[0], func.value[1], func.value[2]
        if self.compareCPU(c) and self.compareRAM(r) and self.compareBW(b):
            # self.map_function(c, r, b) #ToDo <----DONT FORGET TO COMMENT THIS LINE OUT OR EVERYTHING IS GOING TO BE MAPPED.
            # print("NODE {} DOES HAVE SUFFICIENT RESOURCES TO MAP FUNCTION {}\n".format(self.nodeID, func))
            return True
        else:
            # print("NODE {} DOES NOT HAVE SUFFICIENT RESOURCES TO MAP FUNCTION {}\n".format(self.nodeID, func))
            return False

    def check_mappable(self):
        """
        Purpose of this method is to see if a particular
        node has enough resources to map any functions.
        Checks the given nodes available resources and then
        compares them to the cost of each function.

        :return: True if mapping is still possible and False if not.
        """
        costs = FUNCTION_COSTS
        mappable = 0

        for func in costs:
            c = func[0]
            r = func[1]
            b = func[2]

            if self.HELPER_check_enough_resources(c, r, b):
                mappable += 1

        if mappable > 0:
            return True
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
        number_of_failures = n.failure_probability
        number_of_trials = 10
        fail_rate = (number_of_failures + 1) / (number_of_trials + 2)
        return fail_rate

    @staticmethod
    def returnNode(node_id):
        for node in NodeObj.StaticNodeList:
            if node.nodeID == node_id:
                return node

    @staticmethod
    def print_resources(node):
        output = [node.nodeID, node.nodeResources[0], node.nodeResources[1], node.nodeResources[2]]
        return output

    def __str__(self):
        string = "Node ID: {} Node Position: {} Node Status: {} Node Resources: {} Processing Delay: {} Node cost: {} Failure probability: {}".format(
            self.nodeID, (self.nodePosition[0], self.nodePosition[1]), self.status, self.nodeResources,
            self.processingDelay, self.nodeCost, self.failure_probability)
        return string
