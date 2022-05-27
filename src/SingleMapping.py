"""
@author: Jackson Walker
Path resources: [CPU, RAM, Physical buffer size]

Essentially an extension of the request class. Made so that
I can keep track of things specific to a path.

In order to differentiate paths from each-other I am adding specific states that give information on where
the path ranks in usefulness and in the hierarchy of all paths for a specific request.

The criteria for a paths success is the following...
1) Travers-ability
2) Resources capability
3) Within delay threshold
4) within failure threshold
5) Processing

Once the path state is determined the paths are then able to be sorted and used.

PATH_STATE:

OPTIMAL = The best most optimal path for this request. Path that will be mapped.
BACKUP = Path meets all criteria for success but is not the most optimal.
FLUNK = Meets all criteria for success EXCEPT does NOT meet failure threshold.
TURTLE = Meets all criteria for success EXCEPT, delay threshold.
POOR = Path is traversable but does not have enough resources.
STATE_UNKNOWN = The state of the path has yet to be determined.
"""
from src.NodeObj import NodeObj
from src.PathObj import PathObj
from src.VNFObj import VNFObj
from src.LinkObj import LinkObj
from src.RequestObj import RequestObj

from CONSTANTS import GLOBAL_REQUEST_DELAY_THRESHOLD
from CONSTANTS import GlOBAL_FAILURE_THRESHOLD

REQUEST_DELAY_THRESHOLD = GLOBAL_REQUEST_DELAY_THRESHOLD
FAILURE_THRESHOLD = GlOBAL_FAILURE_THRESHOLD
OPTIMAL_PATH_SET = False

# Path Object States
STATE_UNKNOWN = 0
POOR = 1
TURTLE = 2
FLUNK = 3
BACKUP = 4
OPTIMAL = 5


# @Todo need to remember to clear BACKUP_PATHS when finished processing request
def set_path_state_PATH_ONE(path_obj, req_bw, req_vnfs):  # <-- This one DOES NOT use failure probability
    # Given a path must then determine and set the state of the path
    if path_obj.state == STATE_UNKNOWN:
        if calculate_path_resources(path_obj, req_bw, req_vnfs):
            if calculate_path_speed(path_obj, REQUEST_DELAY_THRESHOLD):
                path_obj.state = BACKUP
                PathObj.BACKUP_PATHS.append(path_obj)
            else:
                path_obj.state = TURTLE
                print("PATH {} DELAY {} | PATH IS TOO SLOW!".format(path_obj.pathID, path_obj.DELAY))
        else:
            path_obj.state = POOR
            print("PATH {} DOES NOT HAVE ENOUGH RESOURCES!".format(path_obj.pathID))


def set_path_state_PATH_TWO(path_obj, req_bw, req_vnfs):  # <-- This one DOES use failure probability
    # Given a path must then determine and set the state of the path
    if path_obj.state == STATE_UNKNOWN:
        if calculate_path_resources(path_obj, req_bw, req_vnfs):
            if calculate_path_speed(path_obj, REQUEST_DELAY_THRESHOLD):
                if calculate_path_failure(path_obj, GlOBAL_FAILURE_THRESHOLD):
                    path_obj.state = BACKUP
                    PathObj.BACKUP_PATHS.append(path_obj)
                else:
                    path_obj.state = FLUNK
                    print("PATH {} FAIL {} | PATH FAILURE PROBABILITY TOO HIGH!".format(path_obj.pathID, path_obj.FAILURE_PROBABILITY))
            else:
                path_obj.state = TURTLE
                print("PATH {} DELAY {} | PATH IS TOO SLOW!".format(path_obj.pathID, path_obj.DELAY))
        else:
            path_obj.state = POOR
            print("PATH {} DOES NOT HAVE ENOUGH RESOURCES!".format(path_obj.pathID))


def calculate_path_resources(path_obj, req_bw, req_vnfs):
    """
    Determines if given path has enough resources to satisfy request needs.
        1) Will determine if links in path will meet bandwidth requirements
        2) Will determine if nodes have enough resourcs to map all requested functions

        NOTE: DOES NOT FIND OPTIMAL MAPPING LOCATIONS, SIMPLY DETERMINES IF NODES IN PATH HAVE ENOUGH RESOURCES
              TO MAP EACH FUNCTION AT LEAST ONCE.

    :param path_obj: object holding specific path data
    :param req_bw: The bandwidth needed for this request
    :param req_vnfs: The VNFs needed for this request
    :return: True if path meets resources requirements, False if not.
    """
    req_path_objs = PathObj.create_fusion_obj_list(path_obj.route)
    funcs_to_map = [VNFObj.retrieve_function_value(x) for x in req_vnfs]

    nodes = []  # list of nodes

    for obj in req_path_objs:
        if type(obj) == LinkObj:
            if not obj.check_enough_resources(req_bw):
                banner = "PATH{} LINK {} DID NOT HAVE ENOUGH BANDWIDTH!".format(path_obj.pathID, obj.linkID)
                print(banner)
                return False
        else:
            nodes.append((obj, []))

    for count, lst in enumerate(nodes):  # Determines which nodes we can map
        node = lst[0]
        funcs = lst[1]
        for f in funcs_to_map:  # Fills up funcs with functions we can map to this node
            if node.can_map(f.value):
                funcs.append(f)

        if len(funcs) == 0:  # If we cant map anything we remove it from the list
            nodes.pop(count)

    if len(nodes) == 0:
        banner = "PATH{} DID NOT HAVE ENOUGH RESOURCES TO MAP ANYWHERE PATH FAILS".format(path_obj.pathID)
        print(banner)
        return False
    else:
        for count, lst in enumerate(nodes):  # Now find out if we can map all the VNFs on this route
            node = lst[0]
            funcs = lst[1]
            for i, f in enumerate(funcs_to_map):  # Fills up funcs with functions we can map to this node
                if node.can_map(f.value):
                    funcs_to_map.pop(i)

        if len(funcs_to_map) == 0:
            return True
        else:
            banner = "PATH{} COULD NOT FIND LOCATION TO MAP {}".format(path_obj.pathID, funcs_to_map)
            print(banner)
            return False


def calculate_path_speed(path_obj, delay_threshold):
    """
    Method that is responsible for predicting and calculating the time it would take for a request to be
    processed on a particular path. This method also calculates and sets the values of DELAY and COST for
    each PathObj.

    At this stage every path being processed through this function and beyond meets at least the minimum
    requirements for resources and node mapping.

    RETURN TRUE: Path has proven that it is able to fully process its request within the delay threshold.
    RETURN FALSE: Path is unable to process its request without exceeding the delay threshold.

    1) Need to retrieve needed data from all nodes with mapped functions
    2) Need to retrieve needed data from all links being used
    3) Just have to add it up and make sure its within the threshold

    Things that need to be calculated:
    PATH_COST = node_cost + link_cost
    PATH_DELAY = node_processing_delay + link_edge_delay

    PATH_DELAY <= delay_threshold

    1) Link EdgeDelay
    2) Link EdgeCost
    3) Node Processing Delay for nodes with functions mapped to them
    4) Node cost

    :param path_obj: an object of the PathObj class
    :param delay_threshold: The numerical value representing the window of time to fulfill a request before failure.
    :return: Boolean
    """
    fused_list = PathObj.create_fusion_obj_list(path_obj.route)
    mapping_list = path_obj.MAPPING_LOCATION

    # @ToDo remember that when a function is mapped to a node the delay for that node is: processingDelay + (processingDelay x num_funcs_mapped)
    for mapping_location in mapping_list:
        used_node = mapping_location[0]
        func = mapping_location[1]
        path_obj.DELAY += used_node.processingDelay

    for step in fused_list:
        if type(step) == LinkObj:
            path_obj.DELAY += step.linkED
            path_obj.COST += step.linkEC
        elif type(step) == NodeObj:
            path_obj.DELAY += step.processingDelay
            path_obj.COST += step.nodeCost

    if path_obj.DELAY <= delay_threshold:
        return True
    else:
        return False


def calculate_path_failure(path_obj, failure_threshold):
    failure_rate = path_obj.return_failure_probability()
    if failure_rate <= failure_threshold:
        return True
    else:
        path_obj.state = FLUNK
        print("PATH {} = {} FAILURE PROBABILITY IS TOO HIGH!".format(path_obj.pathID, path_obj.FAILURE_PROBABILITY))
        return False


def calculate_optimal_PATH_ONE():
    """
    Compares every single path that meets all the other specified criteria and finds
    the shortest one WITHOUT the least failure probability.
    """
    if not OPTIMAL_PATH_SET:
        current_best_path = PathObj.BACKUP_PATHS[0]

        for obj in PathObj.BACKUP_PATHS:
            if obj.DELAY < current_best_path.DELAY:
                current_best_path = obj
            elif obj.DELAY == current_best_path.DELAY:
                if obj.COST < current_best_path.COST:
                    current_best_path = obj

        current_best_path.state = 5
        PathObj.OPTIMAL_PATH_SET = True


def calculate_optimal_PATH_TWO():
    """
    Compares every single path that meets all the other specified criteria and finds
    the shortest one WITH the least failure probability.
    """
    if not OPTIMAL_PATH_SET:
        current_best_path = PathObj.BACKUP_PATHS[0]

        for obj in PathObj.BACKUP_PATHS:
            if current_best_path.FAILURE_PROBABILITY < current_best_path.FAILURE_PROBABILITY:
                current_best_path = obj
            elif current_best_path.FAILURE_PROBABILITY == current_best_path.FAILURE_PROBABILITY:
                if obj.DELAY < current_best_path.DELAY:
                    current_best_path = obj
                elif obj.DELAY == current_best_path.DELAY:
                    if obj.COST < current_best_path.COST:
                        current_best_path = obj

        current_best_path.state = 5
        PathObj.OPTIMAL_PATH_SET = True


def map_path_ONE(path_obj):
    if path_obj.state == OPTIMAL:  # Checks to make sure we are mapping the optimal path
        print("MAPPING PATH {}\n".format(path_obj.pathID))
        fused_list = PathObj.create_fusion_obj_list(path_obj.route)
        mapping_list = path_obj.MAPPING_LOCATION
        requested_bandwidth = int(path_obj.REQ_INFO[2])

        for mapping_location in mapping_list:
            node_used = mapping_location[0]
            func = mapping_location[1]
            node_used.map_function_obj(func)

        for element in fused_list:
            if type(element) == LinkObj:
                link = element
                link.map_request(requested_bandwidth)

    node_avg = 0
    link_avg = 0

    for node in NodeObj.StaticNodeList:
        node_avg += node.nodeResources[0]

    for link in NodeObj.StaticLinkList:
        link_avg += link.linkBW

    NodeObj.StaticNodeResources_PATHONE.append(node_avg / 7)
    NodeObj.StaticLinkResources_PATHONE.append(link_avg / 8)
    print("PATH MAPPED")


def map_path_TWO(path_obj):
    if path_obj.state == OPTIMAL:  # Checks to make sure we are mapping the optimal path
        print("MAPPING PATH {}\n".format(path_obj.pathID))
        fused_list = PathObj.create_fusion_obj_list(path_obj.route)
        mapping_list = path_obj.MAPPING_LOCATION
        requested_bandwidth = int(path_obj.REQ_INFO[2])

        for mapping_location in mapping_list:
            node_used = mapping_location[0]
            func = mapping_location[1]
            node_used.map_function_obj(func)

        for element in fused_list:
            if type(element) == LinkObj:
                link = element
                link.map_request(requested_bandwidth)

    node_avg = 0
    link_avg = 0

    for node in NodeObj.StaticNodeList:
        node_avg += node.nodeResources[0]

    for link in NodeObj.StaticLinkList:
        link_avg += link.linkBW

    NodeObj.StaticNodeResources_PATHTWO.append(node_avg / 7)
    NodeObj.StaticLinkResources_PATHTWO.append(link_avg / 8)
    print("PATH MAPPED")


def RUN_PATH_ONE_SINGLE_MAPPING(req):
    req_bw = req.requestedBW
    req_VNFs = req.requestedFunctions

    for path in PathObj.current_request_paths_list:
        set_path_state_PATH_ONE(path, req_bw, req_VNFs)
        if path.state <= 3:
            del path

    if len(PathObj.BACKUP_PATHS) == 0:
        req.requestStatus[0] = 2   # Fail current request if no paths
        RequestObj.STATIC_DENIED_REQUEST_LIST.append(req)

    else:
        req.requestStatus[0] = 3
        RequestObj.STATIC_APPROVED_REQUEST_LIST.append(req)

        calculate_optimal_PATH_ONE()
        optimal_path = PathObj.returnOptimalPath(PathObj.BACKUP_PATHS)
        PathObj.StaticOptimalPathsList.append(optimal_path)
        map_path_ONE(optimal_path)
        req.PATH_ONE = optimal_path

    # Data cleanup process
    PathObj.BACKUP_PATHS.clear()
    PathObj.current_request_paths_list.clear()
    PathObj.current_path_failures.clear()


def RUN_PATH_TWO_SINGLE_MAPPING(req):
    req_bw = req.requestedBW
    req_VNFs = req.requestedFunctions

    for path in PathObj.current_request_paths_list:
        set_path_state_PATH_ONE(path, req_bw, req_VNFs)
        if path.state <= 3:
            del path

    if len(PathObj.BACKUP_PATHS) == 0:
        req.requestStatus[1] = 2  # Fail current request if no paths
        RequestObj.STATIC_DENIED_REQUEST_LIST.append(req)

    else:
        req.requestStatus[1] = 3
        RequestObj.STATIC_APPROVED_REQUEST_LIST.append(req)

        calculate_optimal_PATH_TWO()
        optimal_path = PathObj.returnOptimalPath(PathObj.BACKUP_PATHS)
        PathObj.StaticOptimalPathsList.append(optimal_path)
        map_path_TWO(optimal_path)
        req.PATH_TWO = optimal_path

    # Data cleanup process
    PathObj.BACKUP_PATHS.clear()
    PathObj.current_request_paths_list.clear()
    PathObj.current_path_failures.clear()
