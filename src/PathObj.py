from src.NodeObj import NodeObj
from src.FuncObj import FuncObj
from src.LinkObj import LinkObj
from src.Request import Request

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
BACKUP = Path meets all criteria for success but is not the most optimal
FLUNK = Meets all criteria for success EXCEPT does NOT meet failure threshold
TURTLE = Meets all criteria for success EXCEPT, delay threshold. SHOULD BE NOTED THAT FAILURE THRESHOLD IS NOT CALCULATED FOR THESE PATHS
POOR = Path is traversable but does not have enough resources
STATE_UNKNOWN = The state of the path has yet to be determined.
"""
DELAY_THRESHOLD = 25
OPTIMAL_PATH_SET = False

# Path Object States
STATE_UNKNOWN = 0
POOR = 1
TURTLE = 2
FLUNK = 3
BACKUP = 4
OPTIMAL = 5

"""
For this method I assume the following:
The path parameter is traversable.
The path has enough nodes to map one function per node.
A node can have multiple functions mapped to it but it cannot map multiple functions from the same request.

Return T/F depending on if the path has enough resources to map the function
"""


# @Todo need to be eliminating paths that done meet the standards as they are being processed
# @Todo need to remember to clear BACKUP_PATHS when finished processing request
def set_path_state(path_obj):  # <-- This one DOES NOT use failure probability
    # Given a path must then determine and set the state of the path
    if path_obj.state == STATE_UNKNOWN:
        if calculate_path_resources(path_obj):
            if calculate_path_speed(path_obj, DELAY_THRESHOLD):
                PathObj.BACKUP_PATHS.append(path_obj)
            else:
                path_obj.state = TURTLE
        else:
            path_obj.state = POOR

    # print("PATH {} STATE HAS BEEN SET TO: {}".format(path_obj.pathID, path_obj.state))


def calculate_path_resources(path_obj):
    """
    ToDo need to implement a way for multiple nodes to be mapped to a single function.
    ToDo Need to also factor in link resources as well.

    We can exit the loop and return something when we either:
    1) Know that the path DOES have enough resources, return True.
    2) Know that for whatever reason our functions CANNOT be mapped to the nodes on the path, return False.

    RETURN TRUE: Path has proven that it is able to map every function.
    RETURN FALSE: Destination has been reached before all functions have been mapped.

    :param path_obj: an object of the PathObj class
    :return: Boolean
    """
    fused_path = PathObj.create_fusion_obj_list(path_obj.route)
    funcs_to_map = path_obj.REQ_INFO[0]
    requested_bandwidth = int(path_obj.REQ_INFO[2])
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
            current_node = step    # First we must determine if mapping is even possible
            # print("Node ID: {} Status: {}".format(current_node.nodeID, current_node.status))

            if current_node.status == 'O':
                print("MAPPING ON NODE {} IS NOT POSSIBLE NODE IS OFFLINE".format(current_node.nodeID))
                continue
            elif current_node.status == 'R':
                print("MAPPING ON NODE {} IS NOT POSSIBLE, RELAY TO NEXT NODE IN PATH".format(current_node.nodeID))
                continue
            else:   # Next we need to determine if a node has enough resources for mapping and how many it can handle
                temp_mappable_funcs = current_node.how_many_functions_mappable(funcs_to_map)

                if len(temp_mappable_funcs) == 0 and step == end_node and len(funcs_to_map) > 0:
                    path_obj.state = POOR
                    return False

                elif len(temp_mappable_funcs) == 1:
                    temp_func_list = []
                    current_func = FuncObj.retrieve_function_value(funcs_to_map.pop(0))  # Retrieves the current requested function
                    funcs_mapped.append(current_func)
                    temp_func_list.append(current_func)
                    path_obj.MAPPING_LOCATION.append([current_node, temp_func_list])
                    func_count += 1

                else:   # <---- len(temp_mappable_funcs) > 1
                    temp_func_list = []
                    for i in range(len(temp_mappable_funcs)-1):
                        current_func = FuncObj.retrieve_function_value(funcs_to_map.pop(0))  # Retrieves the current requested function
                        funcs_mapped.append(current_func)
                        temp_func_list.append(current_func)
                        func_count += 1
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
    # ToDo DOES IT MATTER WHAT ORDER THE node_dict and link_dict keys are in if they're all being added up anyway?
    route = path_obj.route
    mapping_list = path_obj.MAPPING_LOCATION

    link_list = []
    PATH_DELAY = 0
    PATH_COST = 0

    """
    Retrieves all the needed data for each link.
    Adds that data to the link_dict
    Ex: { Key : Values } -> { link_name : [ED, EC] } -> { "8->21" : [25, 15] }
    """
    for i in range(len(route) - 1):
        s = route[i]  # Starting node
        d = route[i + 1]  # Destination node

        lnk = LinkObj.returnLink(s, d)
        ED = lnk.linkED
        EC = lnk.linkEC
        link_list.append([ED, EC])

        i += 1

    for l in link_list:
        linkED = l[0]
        linkEC = l[1]

        PATH_DELAY += int(linkED)
        PATH_COST += int(linkEC)

    for temp_list in mapping_list:
        node = temp_list[0]
        funcs = temp_list[1]

        PD = node.processingDelay
        NC = node.nodeCost

        PATH_DELAY += int(PD) * len(funcs)
        PATH_COST += int(NC) * len(funcs)

    # Setting the DELAY and PATH attributes for this PathObj
    path_obj.DELAY = PATH_DELAY
    path_obj.COST = PATH_COST

    if path_obj.DELAY <= delay_threshold:
        return True
    else:
        return False


def calculate_path_failure(path, failure_threshold):
    if path.failure <= failure_threshold:
        return True
    else:
        return False


def calculate_optimal_path():
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


##########################################################################################################################


def map_path(path_obj):
    if path_obj.state == OPTIMAL:   # Checks to make sure we are mapping the optimal path
        print("MAPPING PATH {}\n".format(path_obj.pathID))
        fused_list = PathObj.create_fusion_obj_list(path_obj.route)
        mapping_list = path_obj.MAPPING_LOCATION
        requested_bandwidth = int(path_obj.REQ_INFO[2])

        for element in fused_list:
            if type(element) == LinkObj:
                link = element
                link.map_request(requested_bandwidth)
            else:
                # node = element
                for temp_list in mapping_list:
                    used_node = temp_list[0]
                    funcs = temp_list[1]

                    for f in funcs:
                        used_node.map_function_obj(f)


# ToDo Temporary function I made to test out my methods in this class
def temp_run(paths, req):
    for path in paths:
        set_path_state(path)

    calculate_optimal_path()
    optimal_path = PathObj.returnOptimalPath(PathObj.BACKUP_PATHS)
    tup = (req, optimal_path)

    map_path(optimal_path)

    # Data cleanup process
    PathObj.StaticOptimalPathsList.append(tup)
    PathObj.BACKUP_PATHS.clear()
    PathObj.StaticPathsList.clear()


##########################################################################################################################


class PathObj:
    BACKUP_PATHS = []  # PLACEHOLDER for list of all
    StaticOptimalPathsList = []
    StaticPathsList = []

    def __init__(self, pathID, route, state, REQ_INFO, MAPPING_LOCATION, DELAY, COST):
        """

        :param pathID:
        :param route:
        :param state:
        :param REQ_INFO: [request.requestedFunctions, request.request_delay_threshold, request.requestedBW]
        :param MAPPING_LOCATION: [ NodeObj, [FuncObj] ]
        """
        self.pathID = pathID
        self.route = route
        self.state = state
        self.REQ_INFO = REQ_INFO  # List of all the relevant information needed from the request object for path sorting
        self.MAPPING_LOCATION = MAPPING_LOCATION
        self.DELAY = DELAY
        self.COST = COST

        PathObj.StaticPathsList.append(self)

    @staticmethod
    def create_fusion_obj_list(path):
        links_to_get = []
        output_list = []

        for i in range(len(path) - 1):
            src = path[i]
            dest = path[i + 1]
            link = LinkObj.returnLink(src, dest)
            links_to_get.append(link)
            i += 1

        for n in path:
            node = NodeObj.returnNode(n)
            output_list.append(node)
            if len(links_to_get) != 0:
                link = links_to_get.pop(0)
                output_list.append(link)

        return output_list

    @staticmethod
    def returnOptimalPath(backup_paths_list):
        for path in backup_paths_list:
            if path.state == OPTIMAL:
                return path

    @staticmethod
    def returnPath(id):
        for p in PathObj.StaticPathsList:
            if p.pathID == id:
                return p

    def __str__(self):
        return "Path ID: {} Route: {} State: {} REQ_FUNCTIONS: {} REQ_DELAY_THRESHOLD = {} PATH DELAY: {} PATH COST: {}\n".format(self.pathID, self.route, self.state, self.REQ_INFO[0], self.REQ_INFO[1], self.DELAY, self.COST)
