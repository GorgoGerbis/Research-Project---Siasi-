"""
Node resources: [CPU, RAM, Physical buffer size]
"""


class NodeObj:
    # BE CAREFUL WHEN CHANGING THINGS IN THIS CLASS ITS USED EVERYWHERE
    StaticLinkList = []  # Static List of all links
    StaticNodeList = []  # Static List of all nodes
    TotalNodeCount = 0  # Static variable keeping track of amount of nodes

    def __init__(self, nodeID, nodePosition, status, nodeResources, processingDelay, nodeCost):
        self.nodeID = nodeID
        self.nodePosition = nodePosition
        self.status = status
        # self.nodeResources = nodeResources
        self.nodeCost = nodeCost
        self.processingDelay = processingDelay

        self.nodeResources = nodeResources

        NodeObj.StaticNodeList.append(self)  # <-- APPENDS CURRENT NODE TO STATIC LIST OF ALL NODES

    # Should compile and return a list of all sibling node ids and node objects
    def returnSiblingNodes(self):
        directLinks = []
        output = []

        for link in NodeObj.StaticLinkList:
            linkSrc = link.linkSrc
            linkDest = link.linkDest
            if linkSrc == self.nodeID:
                directLinks.append(link.linkDest)
            elif linkDest == self.nodeID:
                directLinks.append(link.linkSrc)

        # print("Added all direct sibling links to local list")

        for node in NodeObj.StaticNodeList:
            for id in directLinks:
                if node.nodeID == id:
                    output.append(node)

        # print("Added all direct sibling node objects")
        return output

    def areSiblings(self, other):
        # Should probably rewrite this function
        looking = True
        siblings = False

        while looking:
            for link in NodeObj.StaticLinkList:
                if (link.linkSrc == self.nodeID) and (link.linkDest == other.nodeID):
                    looking = False
                    siblings = True
        return siblings

    def returnNode(id):
        for node in NodeObj.StaticNodeList:
            if node.nodeID == id:
                return node

    def __str__(self):
        string = "Node ID: {} Node Position: {} Node Status: {} Node Resources: {} Processing Delay: {} Node cost: {}".format(
            self.nodeID, (self.nodePosition[0], self.nodePosition[1]), self.status, self.nodeResources,
            self.processingDelay, self.nodeCost)
        return string
