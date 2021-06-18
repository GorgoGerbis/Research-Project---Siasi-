from src.NodeObj import NodeObj
from src.FuncObj import FuncObj
from src.LinkObj import LinkObj

"""
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


# Path Object States
STATE_UNKNOWN = 0
POOR = 1
TURTLE = 2
FLUNK = 3
BACKUP = 4
OPTIMAL = 5


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
    route = path_obj.route
    dest = route[-1]

    funcs_to_map = path_obj.REQ_INFO[0]
    fused_path = create_fusion_list(route)

    funcs_mapped = []
    func_count = 0

    for step in route:
        if len(funcs_mapped) == len(funcs_to_map):  # <--- Means we've mapped all the functions
            return True
        elif step == dest and len(funcs_mapped) < len(funcs_to_map):
            path_obj.state = POOR
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
            else:
                if step == dest:
                    path_obj.state = POOR
                    return False


# ToDo I should make some help functions that retrieve all the links and nodes being used in a path.
def get_all_used(path):
    links_to_get = []

    for i in range(len(path) - 1):
        duo = [path[i], path[i + 1]]
        links_to_get.append(duo)
        i += 1

    return links_to_get


def create_fusion_list(path):
    links_to_get = []
    output_list = []

    for i in range(len(path) - 1):
        duo = [path[i], path[i + 1]]
        links_to_get.append(duo)
        i += 1

    for n in path:
        output_list.append(n)
        if len(links_to_get) != 0:
            l = links_to_get.pop(0)
            output_list.append(l)

    return output_list


if __name__ == '__main__':
    path = ['17', '15', '8', '21', '10']
    output = create_fusion_list(path)
    print(output)
