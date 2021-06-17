from src.NodeObj import NodeObj
from src.FuncObj import FuncObj
from src.LinkObj import LinkObj

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
from src.Request import Request

BACKUP_PATHS = []  # PLACEHOLDER for list of all
DELAY_THRESHOLD = 25

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


# def set_path_state(path_obj):  # <-- This one uses Failure probability
#     # Given a path must then determine and set the state of the path
#     while path_obj.state == STATE_UNKNOWN:
#         if calculate_path_resources(path_obj):
#             if calculate_path_speed(path_obj, path_obj.delay):
#                 if calculate_path_failure(path_obj, path_obj.fail):
#                     BACKUP_PATHS.append(path_obj)
#                     calculate_optimal_path()
#                 else:
#                     print("PATH FAILURE PROBABILITY IS TOO HIGH")
#                     path_obj.state = FLUNK
#             else:
#                 print("PATH IS TOO SLOW")
#                 path_obj.state = TURTLE
#         else:
#             print("PATH DOES NOT HAVE ENOUGH RESOURCES")
#             path_obj.state = POOR
#
#     print("PATH STATE HAS BEEN SET!")

# @Todo need to be eliminating paths that done meet the standards as they are being processed
def set_path_state(path_obj):  # <-- This one DOES NOT use failure probability
    # Given a path must then determine and set the state of the path
    while path_obj.state == STATE_UNKNOWN:
        if calculate_path_resources(path_obj):
            if calculate_path_speed(path_obj, path_obj.delay):
                BACKUP_PATHS.append(path_obj)
                calculate_optimal_path()
            else:
                print("PATH IS TOO SLOW")
                path_obj.state = TURTLE
        else:
            print("PATH DOES NOT HAVE ENOUGH RESOURCES")
            path_obj.state = POOR

    print("PATH STATE HAS BEEN SET!")


def calculate_path_failure(path, failure_threshold):
    if path.failure <= failure_threshold:
        return True
    else:
        return False


def calculate_optimal_path():
    for path in BACKUP_PATHS:
        if path.optimal:
            path.state = OPTIMAL
            # BACKUP_PATHS.pop(path)   # Basically if a path is the best one then it
            # gets set as the best one and removed from the PATHS list
        else:
            path.state = BACKUP


##########################################################################################################################
def calculate_path_resources(path_obj):
    """
    We can exit the loop and return something when we either:
    1) Know that the path DOES have enough resources, return True.
    2) Know that for whatever reason our functions CANNOT be mapped to the nodes on the path, return False.

    RETURN TRUE: Path has proven that it is able to map every function.
    RETURN FALSE: Destination has been reached before all functions have been mapped.

    :param path_obj: an object of the PathObj class
    :return: Boolean
    """
    route = path_obj.route
    dest = route[-1]
    funcs_to_map = path_obj.REQ_INFO[0]
    funcs_mapped = []
    func_count = 0

    for step in route:
        if len(funcs_mapped) == len(funcs_to_map):  # <--- Means we've mapped all the functions
            return True
        elif step == dest and len(funcs_mapped) < len(funcs_to_map):
            return False
        else:
            current_node = NodeObj.returnNode(step)  # Retrieves the current requested node for comparison
            current_func = FuncObj.retrieve_function_value(
                funcs_to_map[func_count])  # Retrieves the current requested function

            if current_node.check_enough_resources(current_func):
                # If the current node has enough resources...
                # we PRETEND to map the function to it and continue down the path.
                func_count += 1
                funcs_mapped.append(current_func)
                path_obj.MAPPING_LOCATION.setdefault(step, current_func)
                continue  # We continue on the path.
                # ToDo need to implement a way for multiple nodes to be mapped to a single function


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
    node_dict = path_obj.MAPPING_LOCATION

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

    for key in node_dict:
        current_node = NodeObj.returnNode(key)
        PD = current_node.processingDelay
        NC = current_node.nodeCost

        PATH_DELAY += int(PD)
        PATH_COST += int(NC)

    # Setting the DELAY and PATH attributes for this PathObj
    path_obj.DELAY = PATH_DELAY
    path_obj.COST = PATH_COST

    if path_obj.DELAY <= delay_threshold:
        return True
    else:
        return False


# ToDo Temporary function I made to test out my methods in this class
def temp_run(path_obj):
    calculate_path_resources(path_obj)
    calculate_path_speed(path_obj, DELAY_THRESHOLD)
    print(path_obj)


##########################################################################################################################

class PathObj:

    def __init__(self, pathID, route, state, REQ_INFO, MAPPING_LOCATION, DELAY, COST):
        """

        :param pathID:
        :param route:
        :param state:
        :param REQ_INFO:
        :param MAPPING_LOCATION:
        """
        self.pathID = pathID
        self.route = route
        self.state = state
        self.REQ_INFO = REQ_INFO  # List of all the relevant information needed from the request object for path sorting
        self.MAPPING_LOCATION = MAPPING_LOCATION
        self.DELAY = DELAY
        self.COST = COST

    def __str__(self):
        return "Path ID: {} Route: {} State: {} REQ_FUNCTIONS: {} REQ_DELAY_THRESHOLD = {} PATH DELAY: {} PATH COST: {}".format(self.pathID,
                                                                                                   self.route,
                                                                                                   self.state,
                                                                                                   self.REQ_INFO[0],
                                                                                                   self.REQ_INFO[1],
                                                                                                   self.DELAY,
                                                                                                   self.COST)
