from src.NodeObj import NodeObj
from src.PathObj import PathObj
from src.FuncObj import FuncObj
from src.LinkObj import LinkObj
from src.Request import Request

from ControlPanel import GLOBAL_REQUEST_DELAY_THRESHOLD
from ControlPanel import GlOBAL_FAILURE_THRESHOLD

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
def set_path_state_PATH_ONE(path_obj):  # <-- This one DOES NOT use failure probability
    # Given a path must then determine and set the state of the path
    if path_obj.state == STATE_UNKNOWN:
        if calculate_path_resources_PATH_ONE(path_obj):
            if calculate_path_speed(path_obj, REQUEST_DELAY_THRESHOLD):
                path_obj.state = BACKUP
                PathObj.BACKUP_PATHS.append(path_obj)
            else:
                path_obj.state = TURTLE
                print("PATH {} DELAY {} | PATH IS TOO SLOW!".format(path_obj.pathID, path_obj.DELAY))
        else:
            path_obj.state = POOR
            print("PATH {} DOES NOT HAVE ENOUGH RESOURCES!".format(path_obj.pathID))


# @Todo need to remember to clear BACKUP_PATHS when finished processing request
def set_path_state_PATH_TWO(path_obj):  # <-- This one DOES NOT use failure probability
    # Given a path must then determine and set the state of the path
    if path_obj.state == STATE_UNKNOWN:
        if calculate_path_resources_PATH_TWO(path_obj):
            if calculate_path_speed(path_obj, REQUEST_DELAY_THRESHOLD):
                path_obj.state = BACKUP
                PathObj.BACKUP_PATHS.append(path_obj)
            else:
                path_obj.state = TURTLE
                print("PATH {} DELAY {} | PATH IS TOO SLOW!".format(path_obj.pathID, path_obj.DELAY))
        else:
            path_obj.state = POOR
            print("PATH {} DOES NOT HAVE ENOUGH RESOURCES!".format(path_obj.pathID))


def calculate_path_resources_PATH_ONE(path_obj):
    """
    We can exit the loop and return something when we either:
    1) Know that the path DOES have enough resources, return True.
    2) Know that for whatever reason our functions CANNOT be mapped to the nodes on the path, return False.

    RETURN TRUE: Path has proven that it is able to map every function.
    RETURN FALSE: Destination has been reached before all functions have been mapped.

    :param path_obj: an object of the PathObj class
    :return: Boolean
    """
    fused_path = PathObj.create_fusion_obj_list(path_obj.route)
    req_info = path_obj.REQ_INFO
    funcs_to_map = req_info[0].copy()  # ToDo need to be COPYING LISTS OTHERWISE WE ARE DIRECTLY REFERENCING THEM!
    requested_bandwidth = int(req_info[2])
    end_node = fused_path[-1]

    funcs_mapped = []
    func_count = 0

    for step in fused_path:
        if len(funcs_mapped) != 0 and len(funcs_to_map) == 0:
            return True

        if type(step) == LinkObj:
            # print("Link ID: {} Src: {} Dest: {}".format(step.linkID, step.linkSrc, step.linkDest))
            # NOTE: In HvW Protocol if a link doesnt have enough BW the path fails
            if not step.check_enough_resources(requested_bandwidth):
                path_obj.state = POOR
                return False
        else:
            current_node = step  # First we must determine if mapping is even possible
            # print("Node ID: {} Status: {}".format(current_node.nodeID, current_node.status))

            if current_node.status == 'O':
                # print("MAPPING ON NODE {} IS NOT POSSIBLE NODE IS OFFLINE".format(current_node.nodeID))
                NodeObj.AUTO_FAIL.append(current_node.nodeID)
                path_obj.state = POOR
                return False
            elif current_node.status == 'R':
                # print("MAPPING ON NODE {} IS NOT POSSIBLE, RELAY TO NEXT NODE IN PATH".format(current_node.nodeID))
                continue
            else:  # Next we need to determine if a node has enough resources for mapping and how many it can handle
                temp_mappable_funcs = current_node.how_many_functions_mappable(funcs_to_map) # List of all functions mappable to the current node

                if len(temp_mappable_funcs) == 0 and step.nodeID == end_node.nodeID and len(funcs_to_map) > 0:
                    path_obj.state = POOR
                    return False

                elif len(temp_mappable_funcs) == 1:
                    temp_func_list = []
                    current_func = FuncObj.retrieve_function_value(funcs_to_map.pop(0))# current_func = FuncObj.retrieve_function_value(funcs_to_map.pop(0))  # Retrieves the current requested function
                    funcs_mapped.append(current_func)
                    temp_func_list.append(current_func)
                    path_obj.MAPPING_LOCATION.append([current_node, temp_func_list])
                    func_count += 1

                else:  # <---- len(temp_mappable_funcs) > 1
                    temp_func_list = []
                    for func in temp_mappable_funcs:
                        current_func = FuncObj.retrieve_function_value(funcs_to_map.pop(0))  # Retrieves the current requested function
                        funcs_mapped.append(current_func)
                        temp_func_list.append(current_func)
                        func_count += 1

                    if len(temp_func_list) != 0:
                        path_obj.MAPPING_LOCATION.append([current_node, temp_func_list])


def calculate_path_resources_PATH_TWO(path_obj):
    """
    We can exit the loop and return something when we either:
    1) Know that the path DOES have enough resources, return True.
    2) Know that for whatever reason our functions CANNOT be mapped to the nodes on the path, return False.

    RETURN TRUE: Path has proven that it is able to map every function while being at a stable rate of failure.
    RETURN FALSE: Destination has been reached before all functions have been mapped and/or failure probability is too high.

    :param path_obj: an object of the PathObj class
    :return: Boolean
    """
    fused_path = PathObj.create_fusion_obj_list(path_obj.route)
    req_info = path_obj.REQ_INFO
    funcs_to_map = req_info[0].copy()
    requested_bandwidth = int(req_info[2])
    end_node = fused_path[-1]

    funcs_mapped = []
    func_count = 0

    for step in fused_path:
        if len(funcs_mapped) != 0 and len(funcs_to_map) == 0:
            return True
        if type(step) == LinkObj:
            # NOTE: In HvW Protocol if a link doesnt have enough BW the path fails
            if not step.check_enough_resources(requested_bandwidth):
                path_obj.state = POOR
                return False
            # if step.calculate_failure(step.linkSrc, step.linkDest) >= 0.55:
            #     path_obj.state = FLUNK
            #     return False
        else:
            current_node = step  # First we must determine if mapping is even possible
            # node_failure = NodeObj.calculate_failure(current_node.nodeID)

            # Determining the status of a node and if it has failed
            if current_node.get_status == 'O':
                # print("MAPPING ON NODE {} IS NOT POSSIBLE NODE IS OFFLINE".format(current_node.nodeID))
                NodeObj.AUTO_FAIL_PATH_TWO.append(current_node.nodeID)
                path_obj.state = POOR
                return False
            elif current_node.status == 'R':
                # print("MAPPING ON NODE {} IS NOT POSSIBLE, RELAY TO NEXT NODE IN PATH".format(current_node.nodeID))
                continue
            # elif node_failure >= 0.55:
            #     # print("NODE {} FAILED, MOVING ONTO NEXT NODE IN PATH".format(current_node.nodeID))
            #     PathObj.current_path_failures.append([current_node.nodeID, node_failure])
            #     path_obj.state = POOR
            #     return False
            else:  # Next we need to determine if a node has enough resources for mapping and how many it can handle
                temp_mappable_funcs = current_node.how_many_functions_mappable(funcs_to_map)

                if len(temp_mappable_funcs) == 0:
                    if len(funcs_to_map) > 0 and step.nodeID == end_node.nodeID:
                        path_obj.state = POOR
                        return False
                    if len(funcs_to_map) >= 0 and step.nodeID != end_node.nodeID:
                        continue
                elif len(temp_mappable_funcs) == 1:
                    temp_func_list = []
                    current_func = FuncObj.retrieve_function_value(funcs_to_map.pop(0))  # Retrieves the current requested function
                    funcs_mapped.append(current_func)
                    temp_func_list.append(current_func)
                    path_obj.MAPPING_LOCATION.append([current_node, temp_func_list])
                    func_count += 1

                else:  # <---- len(temp_mappable_funcs) > 1
                    temp_func_list = []
                    for func in temp_mappable_funcs:
                        current_func = FuncObj.retrieve_function_value(funcs_to_map.pop(0))  # Retrieves the current requested function
                        funcs_mapped.append(current_func)
                        temp_func_list.append(current_func)
                        func_count += 1

                    if len(temp_func_list) != 0:
                        path_obj.MAPPING_LOCATION.append([current_node, temp_func_list])


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
        funcs = mapping_location[1]

        for f in funcs:
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
    path_obj.set_failure_probability
    failure_rate = path_obj.FAILURE_PROBABILITY
    if failure_rate <= failure_threshold:
        return True
    else:
        path_obj.state = FLUNK
        print("PATH {} = {}. FAILURE PROBABILITY IS TOO HIGH!".format(path_obj.pathID, path_obj.FAILURE_PROBABILITY))
        return False


def calculate_optimal_PATH_ONE():
    """
    Compares every single path that meets all the other specified criteria and finds
    the shortest one.
    """
    if not OPTIMAL_PATH_SET:
        current_best = PathObj.BACKUP_PATHS[0]

        for path_obj in PathObj.BACKUP_PATHS:
            if path_obj.DELAY < current_best.DELAY:
                current_best = path_obj
            elif path_obj.DELAY == current_best.DELAY:
                if path_obj.COST < current_best.COST:
                    current_best = path_obj

        current_best.state = 5
        PathObj.OPTIMAL_PATH_SET = True

    else:
        reigning_best = PathObj.returnOptimalPath(PathObj.BACKUP_PATHS)

        for path_obj in PathObj.BACKUP_PATHS:
            if path_obj.DELAY < reigning_best.DELAY:
                reigning_best = path_obj
            elif path_obj.DELAY == reigning_best.DELAY:
                if path_obj.COST < reigning_best.COST:
                    reigning_best = path_obj

        reigning_best.state = 5
        PathObj.OPTIMAL_PATH_SET = True


def calculate_optimal_PATH_TWO():
    """
    Compares every single path that meets all the other specified criteria and finds
    the shortest one WITH the least failure probability.
    """
    if not OPTIMAL_PATH_SET:
        current_best = PathObj.BACKUP_PATHS[0]

        for path_obj in PathObj.BACKUP_PATHS:
            path_obj.set_failure_probability()

            if path_obj.FAILURE_PROBABILITY < current_best.FAILURE_PROBABILITY:
                current_best = path_obj
            elif path_obj.FAILURE_PROBABILITY == current_best.FAILURE_PROBABILITY:
                if path_obj.DELAY < current_best.DELAY:
                    current_best = path_obj
                elif path_obj.DELAY == current_best.DELAY:
                    if path_obj.COST < current_best.COST:
                        current_best = path_obj

        current_best.state = 5
        PathObj.OPTIMAL_PATH_SET = True

    else:
        reigning_best = PathObj.returnOptimalPath(PathObj.BACKUP_PATHS)

        for path_obj in PathObj.BACKUP_PATHS:
            path_obj.set_failure_probability()

            if path_obj.FAILURE_PROBABILITY < reigning_best.FAILURE_PROBABILITY:
                reigning_best = path_obj
            elif path_obj.FAILURE_PROBABILITY == reigning_best.FAILURE_PROBABILITY:
                if path_obj.DELAY < reigning_best.DELAY:
                    reigning_best = path_obj
                elif path_obj.DELAY == reigning_best.DELAY:
                    if path_obj.COST < reigning_best.COST:
                        reigning_best = path_obj

        reigning_best.state = 5
        PathObj.OPTIMAL_PATH_SET = True


def map_path_ONE(path_obj):
    if path_obj.state == OPTIMAL:  # Checks to make sure we are mapping the optimal path
        print("MAPPING PATH {}\n".format(path_obj.pathID))
        fused_list = PathObj.create_fusion_obj_list(path_obj.route)
        mapping_list = path_obj.MAPPING_LOCATION
        requested_bandwidth = int(path_obj.REQ_INFO[2])

        for mapping_location in mapping_list:
            node_used = mapping_location[0]
            funcs_to_map = mapping_location[1]
            for f in funcs_to_map:
                node_used.map_function_obj(f)

        for element in fused_list:
            if type(element) == LinkObj:
                link = element
                link.map_request(requested_bandwidth)


    print("PATH MAPPED")


def map_path_TWO(path_obj):
    if path_obj.state == OPTIMAL:  # Checks to make sure we are mapping the optimal path
        print("MAPPING PATH {}\n".format(path_obj.pathID))
        fused_list = PathObj.create_fusion_obj_list(path_obj.route)
        mapping_list = path_obj.MAPPING_LOCATION
        requested_bandwidth = int(path_obj.REQ_INFO[2])

        for mapping_location in mapping_list:
            node_used = mapping_location[0]
            funcs_to_map = mapping_location[1]
            for f in funcs_to_map:
                node_used.map_function_obj(f)

        for element in fused_list:
            if type(element) == LinkObj:
                link = element
                link.map_request(requested_bandwidth)


    print("PATH MAPPED")

def RUN_PATH_ONE(req):
    for path in PathObj.current_request_paths_list:
        # print(path)
        set_path_state_PATH_ONE(path)

    if len(PathObj.BACKUP_PATHS) == 0:
        req.requestStatus[0] = 2   # Fail current request if no paths
        Request.STATIC_DENIED_REQUEST_LIST.append(req)

    else:
        req.requestStatus[0] = 3
        Request.STATIC_APPROVED_REQUEST_LIST.append(req)

        calculate_optimal_PATH_ONE()
        optimal_path = PathObj.returnOptimalPath(PathObj.BACKUP_PATHS)
        PathObj.StaticOptimalPathsList.append(optimal_path)
        map_path_ONE(optimal_path) # map_path_PATH_ONE(optimal_path)
        req.PATH_ONE = optimal_path

    # Data cleanup process
    PathObj.BACKUP_PATHS.clear()
    PathObj.current_request_paths_list.clear()
    # PathObj.StaticPathsList.clear()


def RUN_PATH_TWO(req):
    for path in PathObj.current_request_paths_list:
        # print(path)
        set_path_state_PATH_TWO(path)

    if len(PathObj.BACKUP_PATHS) == 0:
        req.requestStatus[1] = 2  # Fail current request if no paths
        Request.STATIC_DENIED_REQUEST_LIST.append(req)

    else:
        req.requestStatus[1] = 3
        Request.STATIC_APPROVED_REQUEST_LIST.append(req)

        calculate_optimal_PATH_TWO()
        optimal_path = PathObj.returnOptimalPath(PathObj.BACKUP_PATHS)
        PathObj.StaticOptimalPathsList.append(optimal_path)
        map_path_TWO(optimal_path) # map_path_PATH_TWO(optimal_path)
        req.PATH_TWO = optimal_path

    # Data cleanup process
    PathObj.BACKUP_PATHS.clear()
    PathObj.current_request_paths_list.clear()
    PathObj.current_path_failures.clear()
    # PathObj.StaticPathsList.clear()
