"""
IGNORE THIS FILE...
THIS IS A BLANK CANVAS TO FOR CLEANING UP NEW FUNCTIONS/METHODS IN AN EASIER TO MANAGE/READ ENVIRONMENT
"""
from src.VNFObj import VNFObj
from src.NodeObj import NodeObj


def what_can_node_map_at_once(self, vnfs=None):  # <--- Allows me to overload this
    """
    Will return the VNFs that can all be mapped at once to this particular node.
    :param vnfs: optional argument, if not specifying the VNFs to check then simply check all VNF types.
    :return: List of all VNFs you can map
    """
    mappable_at_once = []

    cpu = self.nodeResources[0]
    ram = self.nodeResources[1]

    total_req_cpu = 0
    total_req_ram = 0

    if vnfs is None:
        all_possible_vnfs = [e.value for e in VNFObj]
    else:
        all_possible_vnfs = vnfs.copy()

    for f in all_possible_vnfs:
        total_req_cpu += f.value[0]
        total_req_ram += f.value[1]
        if (total_req_cpu <= cpu) and (total_req_ram <= ram):
            mappable_at_once.append(f)

    return mappable_at_once


def determine_optimal_mapping_location(node_options, vnfs, protocol):
    """
    How do I want to handle this??
    Should we be fully greedy and just map in perfect scenarios only??
    Do we map in other locations if possible?
    :param node_options:
    :param vnfs:
    :param protocol:
    :return:
    """
    left, right = 0, len(node_options) - 1
    output = []

    if protocol == 1:  # SINGLE MAPPING
        output = perfect_world_single(node_options, vnfs.copy())
        print(output)

    if protocol == 2:
        output = perfect_world_multi(node_options, vnfs.copy())
        print(output)


# def perfect_world_single(node_options, vnfs):
#     output = []
#     for element in node_options: # We are mapping as many as possible on each node
#         node = element[0]
#         funcs = element[1]
#         temp = []
#
#         if len(vnfs) == 0:
#             break
#         else:
#             if len(funcs) != 0:
#                 for f in funcs:
#                     if f in vnfs:
#                         temp.append(f)
#                         vnfs.remove(f)
#
#                 if len(temp) != 0:
#                     output.append([node, temp])
#
#     return output


def perfect_world_single(node_options, vnfs):
    output = []
    left = 0
    i = 0
    while i < len(vnfs):
        if left > len(node_options) - 1:    # <-- Resetting and starting at top of queue again....
            left = 0



def perfect_world_multi(node_options, vnfs):
    """
    WIll TRY TO MAP ONE VNF PER NODE IF POSSIBLE
    IF NOT WILL KEEP LOOPING MAPPING ANY MISSING VNFS ON THE NEXT NODE IN LINE.

    Todo: SHOULD I map on each spot or map on the last item if possible?

    EX: dataset5 = [[1, []], [2, []], [3, ['f1', 'f2', 'f3']], [4, ['f1', 'f2', 'f3']]]
    OUTPUT: [3, f1], [4, f2], [3, f3]

    :param node_options:
    :param vnfs:
    :return:
    """
    output = []
    left = 0
    i = 0
    while i < len(vnfs):    # <-- Resetting and starting at top of queue again....
        if left > len(node_options) - 1:
            left = 0

        current_element = node_options[left]
        node = current_element[0]
        funcs = current_element[1]
        f = vnfs[i]

        if f in funcs:
            output.append([node, f])
            i += 1
        left += 1

    return output


def calculate_path_resources(path_obj, req_bw, req_vnfs):   # <-- MULTI-MAPPING
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
    route = path_obj.route
    req_path_objs = PathObj.create_fusion_obj_list(route)
    funcs_to_map = [VNFObj.retrieve_function_value(e) for e in req_vnfs]

    nodes = []  # list of nodes

    if not PathObj.check_path_link_bandwidth(route, req_bw):    # <-- Do the links have enough bandwidth?
        print("PATH:{} NOT ENOUGH LINK BANDWIDTH\n".format(path_obj.pathID))
        return False

    if not PathObj.check_path_node_resources(route, req_vnfs):  # <-- Can we map each VNF once?
        print("PATH:{} NOT ENOUGH RESOURCES\n".format(path_obj.pathID))

    # for count, lst in enumerate(nodes):  # Determines which nodes we can map
    #     node = lst[0]
    #     mappable = node.what_can_node_map_at_once(funcs_to_map)
    #     nodes[count][1] = mappable
    #
    #     if len(mappable) == 0:  # If we cant map anything we remove it from the list
    #         nodes.pop(count)
    #
    # if len(nodes) == 0:
    #     banner = "PATH{} DID NOT HAVE ENOUGH RESOURCES TO MAP ANYWHERE PATH FAILS".format(path_obj.pathID)
    #     print(banner)
    #     return False
    # else:
    #     for count, lst in enumerate(nodes):  # Now find out if we can map all the VNFs on this route
    #         node = lst[0]
    #         for i, f in enumerate(funcs_to_map):  # Fills up funcs with functions we can map to this node
    #             if node.can_map(f.value):
    #                 funcs_to_map.pop(i)
    #
    #     if len(funcs_to_map) == 0:
    #         PathObj.determine_optimal_mapping_location(nodes, req_vnfs, 2)
    #         return True
    #     else:
    #         banner = "PATH{} COULD NOT FIND LOCATION TO MAP {}".format(path_obj.pathID, funcs_to_map)
    #         print(banner)
    #         return False


if __name__ == '__main__':
    dataset1 = [[1, ['f1', 'f2', 'f3']], [2, ['f1', 'f2', 'f3']], [3, ['f1', 'f2', 'f3']], [4, ['f1', 'f2', 'f3']]]     # path should work
    dataset2 = [[1, ['f2', 'f3']], [2, []], [3, ['f3']], [4, ['f1', 'f3']]]     # path should work
    dataset3 = [[1, ['f2']], [2, ['f1']], [3, ['f3']], [4, []]]     # Path should fail
    dataset4 = [[1, []], [2, []], [3, ['f1', 'f2', 'f3']], [4, []]]     # Path should work
    dataset5 = [[1, []], [2, []], [3, ['f1', 'f2', 'f3']], [4, ['f1', 'f2', 'f3']]]

    vnfs = ['f1', 'f2', 'f3']

    what_can_node_map()

    # determine_optimal_mapping_location(dataset1, vnfs, 1)
    # determine_optimal_mapping_location(dataset2, vnfs, 1)
    # determine_optimal_mapping_location(dataset3, vnfs, 1)
    # determine_optimal_mapping_location(dataset4, vnfs, 1)

    # determine_optimal_mapping_location(dataset1, vnfs, 2)
    # determine_optimal_mapping_location(dataset2, vnfs, 2)
    # determine_optimal_mapping_location(dataset3, vnfs, 2)
    # determine_optimal_mapping_location(dataset4, vnfs, 2)
    # determine_optimal_mapping_location(dataset5, vnfs, 2)
