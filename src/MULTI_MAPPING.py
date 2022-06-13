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

from CONSTANTS import GLOBAL_REQUEST_DELAY_THRESHOLD as REQUEST_DELAY_THRESHOLD
from CONSTANTS import GlOBAL_FAILURE_THRESHOLD as FAILURE_THRESHOLD
from CONSTANTS import CREATE_NUM_NODES, CREATE_NUM_LINKS, CREATE_NUM_REQUESTS
OPTIMAL_PATH_SET = False

# Path Object States
STATE_UNKNOWN = 0
POOR = 1
TURTLE = 2
FLUNK = 3
BACKUP = 4
OPTIMAL = 5


# @Todo need to remember to clear BACKUP_PATHS when finished processing request
def set_path_state_PATH_ONE(path_obj, req_VNFs):  # <-- This one DOES NOT use failure probability
    # Given a path must then determine and set the state of the path
    if path_obj.state == STATE_UNKNOWN:
        if calculate_path_resources(path_obj, req_VNFs):
            path_obj.MAPPING_LOCATION = path_obj.determine_mapping_location_multi(req_VNFs)
            if calculate_path_speed(path_obj, REQUEST_DELAY_THRESHOLD):
                path_obj.state = BACKUP
                PathObj.BACKUP_PATHS.append(path_obj)
            else:
                path_obj.state = TURTLE
                print("PATH {} DELAY {} | PATH IS TOO SLOW!".format(path_obj.pathID, path_obj.DELAY))
        else:
            path_obj.state = POOR
            print("PATH {} DOES NOT HAVE ENOUGH RESOURCES!".format(path_obj.pathID))


def set_path_state_PATH_TWO(path_obj, req_VNFs):  # <-- This one DOES use failure probability
    # Given a path must then determine and set the state of the path
    if path_obj.state == STATE_UNKNOWN:
        if calculate_path_resources(path_obj, req_VNFs):
            path_obj.MAPPING_LOCATION = path_obj.determine_mapping_location_multi(req_VNFs)
            if calculate_path_speed(path_obj, REQUEST_DELAY_THRESHOLD):
                if calculate_path_failure(path_obj, FAILURE_THRESHOLD):
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


def calculate_path_resources(path_obj, req_vnfs):  # <-- MULTI-MAPPING
    """
    Determines if given path has enough resources to satisfy request needs.
        1) Will determine if links in path will meet bandwidth requirements
        2) Will determine if nodes have enough resourcs to map ALL requested functions

        NOTE: DOES NOT FIND OPTIMAL MAPPING LOCATIONS, SIMPLY DETERMINES IF NODES IN PATH HAVE ENOUGH RESOURCES
              TO MAP EACH FUNCTION AT LEAST ONCE.

    :param path_obj: object holding specific path data
    :param req_bw: The bandwidth needed for this request
    :param req_vnfs: The VNFs needed for this request
    :return: True if path meets resources requirements, False if not.
    """
    if not path_obj.check_path_link_bandwidth():  # <-- Do the links have enough bandwidth?
        print("PATH:{} NOT ENOUGH LINK BANDWIDTH\n".format(path_obj.pathID))
        return False

    if not path_obj.check_path_node_resources(req_vnfs):  # <-- Can we map each VNF once?
        print("PATH:{} NOT ENOUGH RESOURCES\n".format(path_obj.pathID))
        return False

    return True


def calculate_path_speed(path_obj, delay_threshold):
    fused_list = PathObj.create_fusion_obj_list(path_obj.route)
    mapping_list = path_obj.MAPPING_LOCATION

    # @ToDo remember that when a function is mapped to a node the delay for that node is: processingDelay + (processingDelay x num_funcs_mapped)
    for elements in mapping_list:
        used_node = elements[0]
        func = elements[1]  # Unused variable holing func information....
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
            if obj.FAILURE_PROBABILITY < current_best_path.FAILURE_PROBABILITY:
                current_best_path = obj
            elif obj.FAILURE_PROBABILITY == current_best_path.FAILURE_PROBABILITY:
                if obj.DELAY < current_best_path.DELAY:
                    current_best_path = obj
                elif obj.DELAY == current_best_path.DELAY:
                    if obj.COST < current_best_path.COST:
                        current_best_path = obj

        current_best_path.state = 5
        PathObj.OPTIMAL_PATH_SET = True


def map_path(path_obj, req_bw):
    if path_obj.state == OPTIMAL:  # Checks to make sure we are mapping the optimal path
        print("MAPPING PATH {}\n".format(path_obj.pathID))
        fused_list = PathObj.create_fusion_obj_list(path_obj.route)
        mapping_list = path_obj.MAPPING_LOCATION

        for element in mapping_list: # @TODO YOU CAN NOT! EDIT THE CLASS RESOURCES HERE NEED TO DO IT IN PROCESSING DATA SCRIPT MANUALLY
            node_used = element[0]
            func = element[1]
            node_used.map_function_obj(func)

        for element in fused_list:
            if type(element) == LinkObj:
                link = element
                link.map_request(req_bw)

    node_avg = 0
    link_avg = 0

    for node in NodeObj.StaticNodeList:
        node_avg += node.nodeResources[0]

    for link in NodeObj.StaticLinkList:
        link_avg += link.linkBW

    NodeObj.StaticNodeResources_PATHONE.append(node_avg / CREATE_NUM_NODES)
    NodeObj.StaticLinkResources_PATHONE.append(link_avg / CREATE_NUM_LINKS)
    print("PATH {} MAPPED".format(path_obj.pathID))


def RUN_PATH_ONE(req):
    req_bw = req.requestedBW
    req_VNFs = req.requestedFunctions

    for path in PathObj.current_request_paths_list:
        set_path_state_PATH_ONE(path, req_VNFs)
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
        map_path(optimal_path, req_bw)
        req.PATH_ONE = optimal_path

    # Data cleanup process
    PathObj.BACKUP_PATHS.clear()
    PathObj.current_request_paths_list.clear()
    PathObj.current_path_failures.clear()


def RUN_PATH_TWO(req):
    req_bw = req.requestedBW
    req_VNFs = req.requestedFunctions

    for path in PathObj.current_request_paths_list:
        set_path_state_PATH_ONE(path, req_VNFs)
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
        map_path(optimal_path, req_bw)
        req.PATH_TWO = optimal_path

    # Data cleanup process
    PathObj.BACKUP_PATHS.clear()
    PathObj.current_request_paths_list.clear()
    PathObj.current_path_failures.clear()
