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


def set_path_state(path_obj):
    # Given a path must then determine and set the state of the path
    while path_obj.state == STATE_UNKNOWN:
        if calculate_path_resources(path_obj):
            if calculate_path_speed(path_obj, path_obj.delay):
                if calculate_path_failure(path_obj, path_obj.fail):
                    BACKUP_PATHS.append(path_obj)
                    calculate_optimal_path()
                else:
                    print("PATH FAILURE PROBABILITY IS TOO HIGH")
                    path_obj.state = FLUNK
            else:
                print("PATH IS TOO SLOW")
                path_obj.state = TURTLE
        else:
            print("PATH DOES NOT HAVE ENOUGH RESOURCES")
            path_obj.state = POOR

    print("PATH STATE HAS BEEN SET!")


def calculate_path_speed(path, delay_threshold):
    if path.speed <= delay_threshold:
        return True
    else:
        return False


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


# def calculate_path_resources(path_obj):
#     """
#     We can exit the loop and return something when we either:
#     1) Know that the path DOES have enough resources, return True.
#     2) Know that for whatever reason our functions CANNOT be mapped to the nodes on the path, return False.
#
#     RETURN TRUE: Path has proven that it is able to map every function.
#     RETURN FALSE: Destination has been reached before all functions have been mapped.
#
#     :param path_obj: an object of the PathObj class
#     :return: Boolean
#     """
#     route = path_obj.route
#     funcs = path_obj.REQ_INFO[0]
#     dest = path_obj.route[-1]  # Retrieves the last element in the route list
#
#     funcs_mapped = []
#
#     func_count = 0
#
#     for step in route:
#
#         if step == dest and len(funcs_mapped) < len(funcs):
#             return False
#
#         elif len(funcs_mapped) == len(funcs):
#             return True
#
#         else:
#             current_node = NodeObj.returnNode(step)  # Retrieves the current requested node for comparison
#             current_func = FuncObj.retrieve_function_value(funcs[func_count])  # Retrieves the current requested function
#
#             if current_node.check_enough_resources(current_func):
#                 # If the current node has enough resources...
#                 # we PRETEND to map the function to it and continue down the path.
#                 funcs_mapped.append(current_func)
#                 continue  # We continue on the path.


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
    funcs = path_obj.REQ_INFO[0]
    # dest = path_obj.route[-1] # <--- If this option works better I wont even need this  # Retrieves the last element in the route list

    funcs_mapped = []

    func_count = 0

    for step in route:
        current_node = NodeObj.returnNode(step)  # Retrieves the current requested node for comparison
        current_func = FuncObj.retrieve_function_value(funcs[func_count])  # Retrieves the current requested function

        if current_node.check_enough_resources(current_func):
            # If the current node has enough resources...
            # we PRETEND to map the function to it and continue down the path.
            funcs_mapped.append(current_func)
            continue  # We continue on the path.

    # I moved these to after the loop bc it just feels cleaner this way
    if len(funcs_mapped) == len(funcs):
        return True
    elif len(funcs_mapped) < len(funcs):
        return False


# ToDo Temporary function I made to test out my methods in this class
def temp_run(path_obj):
    calculate_path_resources(path_obj)
    # if calculate_path_resources(path_obj):
    #     print("PATH {} HAS ENOUGH RESOURCES AND WILL MOVE ON".format(path_obj.pathID))
    # else:
    #     print("PATH {} DOES NOT HAVE ENOUGH RESOURCES AND WILL NOT MOVE ON".format(path_obj.pathID))


##########################################################################################################################

class PathObj:

    def __init__(self, pathID, route, state, REQ_INFO):
        self.pathID = pathID
        self.route = route
        self.state = state

        # Warning this will probably be super finicky
        self.REQ_INFO = REQ_INFO  # List of all the relevant information needed from the request object for path sorting

    def __str__(self):
        return "Path ID: {} Route: {} State: {} REQ_FUNCTIONS: {} REQ_DELAY_THRESHOLD = {}".format(self.pathID,
                                                                                                   self.route,
                                                                                                   self.state,
                                                                                                   self.REQ_INFO[0],
                                                                                                   self.REQ_INFO[1])
