# MY OWN CLASSES
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.Request import Request


# ToDo need to find a way to constantly feed the path that is currently being processed on.

# This checks to see if the path is possible resource-wise
# def calculate_path(req, node, link):
# Get the current stats from the req
# Can node handle it?
# Does link have enough BW?

# Update all
# Push request forward or deny request

def calculate_path(req, node, link):
    functions = req.functions
    bw = req.requestedBW
    status = req.requestStatus
    return


def find_specific_data(reqId, nodeId, linkId):
    not_done = True

    a = False
    b = False
    c = False

    # node = NodeObj()
    # link = LinkObj()
    # req = Request()

    while not_done:
        if a and b and c:
            break

        for n in NodeObj.StaticNodeList:
            if n.nodeID == nodeId:
                node = n
                a = True

        for l in LinkObj.StaticLinkList:
            if l.linkID == linkId:
                link = l
                b = True

        for r in Request.StaticTotalRequestList:
            if r.requestID == reqId:
                req = r
                c = True

    print("Found data! ReqID: {} NodeID: {} LinkID: {}".format(req.requestID, node.nodeID, link.linkID))

    return req, node, link
