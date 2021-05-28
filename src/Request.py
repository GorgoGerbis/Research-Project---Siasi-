from src.NodeObj import NodeObj


class Request():
    # Purpose of this class is to take in requests and calculate the amount of resources required as well as time delay

    StaticTotalRequestList = []
    staticApprovedRequestList = []

    REQUEST_NEEDS_CALCULATING = 0
    REQUEST_DENIED = 1
    REQUEST_APPROVED = 2

    def __init__(self, requestID, source, destination, requestedFunctions, requestedBW, requestStatus):
        self.requestID = requestID
        self.source = source
        self.destination = destination
        self.requestedFunctions = requestedFunctions
        self.requestedBW = requestedBW
        self.requestStatus = requestStatus

    def calculateRequestPossibility(self):
        pointA = self.source
        pointANode = NodeObj.giveRequestedNode(self.source)
        pointB = self.destination
        pointBNode = NodeObj.giveRequestedNode(self.destination)

        if (pointANode and pointBNode) in NodeObj.StaticNodeList:
            print("Request {} source node and destination node both exist.".format(self.requestID))


        else:
            print("Request {} source node and/or destination node do not exist.".format(self.requestID))

    # def calculateRequestFunctionCost(self):

    def __str__(self):
        return "REQUEST NUMBER: {} REQUEST SOURCE: {} REQUESTED DESTINATION: {} REQUESTED FUNCTIONS: {} REQUESTED BANDWIDTH: {}".format(
            self.requestID, self.source, self.destination, self.requestedFunctions, self.requestedBW)
