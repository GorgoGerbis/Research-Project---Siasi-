class NodeObj:
    StaticLinkList = []  # Static List of all links
    StaticNodeList = []  # Static List of all nodes
    TotalNodeCount = 0   # Static variable keeping track of amount of nodes

    def __init__(self, nodeID, nodePosition, status, nodeResources, processingDelay, nodeCost):
        self.nodeID = nodeID
        self.nodePosition = nodePosition
        self.status = status
        self.nodeResources = nodeResources
        self.processingDelay = processingDelay
        self.nodeCost = nodeCost

        self.connectedLinks = [] # List of all links that have this node as Source
        NodeObj.StaticNodeList.append(self)
        NodeObj.TotalNodeCount += 1  # Increases the total node count

        self.siblingLinks = []
        self.siblingNodes = []

    def isIsolated(self):
        if len(self.siblingLinks) == 0:
            return True

    def findSiblings(self):
        for link in NodeObj.StaticLinkList:
            if link.linkDest == self.nodeID:
                self.siblingLinks.append(link)

        for link in self.siblingLinks:
            current_link = link.linkSrc
            for node in NodeObj.StaticNodeList:
                if node.ID == current_link:
                    self.siblingNodes.append(node.ID)


    def addLinksToNetwork(self, linkObj):
        self.connectedLinks.append(linkObj)

    def printConnectedLinks(self):
        for obj in self.connectedLinks:
            print("Link: " + str(obj))

    def giveRequestedNode(idNum):
        for obj in NodeObj.staticNodeList:
            if obj.nodeID == idNum:
                return obj

    def areSiblings(self, other):
        looking = True
        siblings = False

        while looking:
            for link in NodeObj.StaticLinkList:
                if (link.linkSrc == self.nodeID) and (link.linkDest == other.nodeID):
                    looking = False
                    siblings = True
        return siblings

    def __str__(self):
        # string = "Node ID: {} Node Position: {} Node Status: {} Node Resources: {} Processing Delay: {} Node cost: {}".format(self.nodeID, self.nodePosition, self.status, self.nodeResources, self.nodeCost)
        string = "NODE ID: " + self.nodeID
        return string
