"""
Node resources: [CPU, RAM, Physical buffer size]
"""


class NodeObj:
    # BE CAREFUL WHEN CHANGING THINGS IN THIS CLASS ITS USED EVERYWHERE
    StaticLinkList = []  # Static List of all links
    StaticNodeList = []  # Static List of all nodes
    TotalNodeCount = 0  # Static variable keeping track of amount of nodes

    def __init__(self, nodeID, nodePosition, status, nodeResources, processingDelay, nodeCost, failureProbablity):
        self.nodeID = nodeID
        self.nodePosition = nodePosition
        self.status = status
        self.nodeCost = nodeCost
        self.processingDelay = processingDelay

        self.nodeResources = nodeResources
        self.failureProbablity = failureProbablity

        NodeObj.StaticNodeList.append(self)  # <-- APPENDS CURRENT NODE TO STATIC LIST OF ALL NODES

    def returnNode(id):
        for node in NodeObj.StaticNodeList:
            if node.nodeID == id:
                return node

    def compareCPU(self, cpu):
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

    def __str__(self):
        string = "Node ID: {} Node Position: {} Node Status: {} Node Resources: {} Processing Delay: {} Node cost: {} Failure probability: {}".format(
            self.nodeID, (self.nodePosition[0], self.nodePosition[1]), self.status, self.nodeResources,
            self.processingDelay, self.nodeCost, self.failureProbablity)
        return string
