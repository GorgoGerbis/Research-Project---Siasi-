from src.FuncObj import FuncObj
"""
@author: Jackson Walker
"""


class NodeObj:
    # BE CAREFUL WHEN CHANGING THINGS IN THIS CLASS ITS USED EVERYWHERE
    StaticLinkList = []  # Static List of all links
    StaticNodeList = []  # Static List of all nodes
    TotalNodeCount = 0  # Static variable keeping track of amount of nodes

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
        return neighbors

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

    # This method has to be static so that it can be accessed everywhere basically just a helper function
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
