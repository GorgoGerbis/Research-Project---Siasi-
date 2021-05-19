# MY OWN CLASSES
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.Request import Request
from src.FuncObj import FuncObj


# ToDo need to find a way to constantly feed the path that is currently being processed on.
# Todo will need to find a way to accurately calculate the physical buffer size

# This checks to see if the path is possible resource-wise
# def calculate_path(req, node, link):
# Get the current stats from the req
# Can node handle it?
# Does link have enough BW?

# Update all
# Push request forward or deny request

def calculate_path(req, node, link):
    req_functions = req.requestedFunctions
    req_bw = req.requestedBW
    req_status = req.requestStatus

    node_ID = node.nodeID
    node_status = node.status

    calculate_node_resources(req, node)     # <-- For testing purposes will remove this later

    return


# Todo need to add a function that essentially tells the path finder to skip this node and move on the next one.
def calculate_node_resources(req, node):
    node_resources = node.nodeResources
    # node_resources_CPU = node_resources[0]
    # node_resources_RAM = node_resources[1]
    node_processing_delay = node.processingDelay
    node_cost = node.nodeCost

    for func in req.requestedFunctions:
        current_func = func
        print()

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
