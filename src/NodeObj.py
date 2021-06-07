"""
@author: Jackson Walker
Node resources: [CPU, RAM, Physical buffer size]
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
        if int(self.nodeResources[0]) >= cpu:
            return True
        else:
            return False

    def compareRAM(self, ram):
        if int(self.nodeResources[1]) >= ram:
            return True
        else:
            return False

    def compareBW(self, bw):
        if int(self.nodeResources[2]) >= bw:
            return True
        else:
            return False

    def map_function(self, cpu, ram, bw):
        self.nodeResources[0] = int(self.nodeResources[0]) - cpu
        self.nodeResources[1] = int(self.nodeResources[1]) - ram
        self.nodeResources[2] = int(self.nodeResources[2]) - bw

    def check_enough_resources(self, func):
        c, r, b = func[0], func[1], func[2]
        if self.compareCPU(c) and self.compareRAM(r) and self.compareBW(b):
            self.map_function(c, r, b)
            print("FUNCTION HAS BEEN MAPPED")
            return 0
        else:
            print("NODE DOES NOT HAVE ENOUGH RESOURCES")
            return

    # This method has to be static so that it can be accessed everywhere basically just a helper function
    @staticmethod
    def returnNode(node_id):
        for node in NodeObj.StaticNodeList:
            if node.nodeID == node_id:
                return node

    @staticmethod
    def print_resources(node):
        # output = [CPU, RAM, Physical Buffer Size]
        output = [node.nodeID, node.nodeResources[0], node.nodeResources[1], node.nodeResources[2]]
        return output

    def __str__(self):
        string = "Node ID: {} Node Position: {} Node Status: {} Node Resources: {} Processing Delay: {} Node cost: {} Failure probability: {}".format(
            self.nodeID, (self.nodePosition[0], self.nodePosition[1]), self.status, self.nodeResources,
            self.processingDelay, self.nodeCost, self.failure_probability)
        return string
