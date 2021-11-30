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
    end_link = fused_path[-2]

    enough_bw = False
    all_mapped = False

    funcs_mapped = []
    func_count = 0

    for step in fused_path:
        if all_mapped and enough_bw:
            return True
        if type(step) == LinkObj:
            # print("Link ID: {} Src: {} Dest: {}".format(step.linkID, step.linkSrc, step.linkDest))
            # NOTE: In HvW Protocol if a link doesnt have enough BW the path fails
            check_bw = step.check_enough_resources(requested_bandwidth)
            if not check_bw:
                path_obj.state = POOR
                return False
            elif step.linkID == end_link.linkID:
                enough_bw = True
        else:
            if all_mapped:
                continue
            else:
                current_node = step  # First we must determine if mapping is even possible

                # if current_node.nodeID in AUTO_FAIL:
                #     path_obj.state = POOR
                #     return False
                if current_node.status == 'O':
                    # print("MAPPING ON NODE {} IS NOT POSSIBLE NODE IS OFFLINE".format(current_node.nodeID))
                    NodeObj.AUTO_FAIL.append(current_node.nodeID)
                    path_obj.state = POOR
                    return False
                elif current_node.status == 'R':
                    continue
                else:  # Next we need to determine if a node has enough resources for mapping and how many it can handle

                    if len(funcs_to_map) == 0:
                        all_mapped = True
                        continue
                    else:
                        current_func = funcs_to_map[0]
                        mappable = current_node.check_enough_resources(current_func)

                        if not mappable and step.nodeID == end_node.nodeID and len(funcs_to_map) > 0:
                            path_obj.state = POOR
                            return False
                        elif mappable:
                            funcs_mapped.append(current_func)
                            path_obj.MAPPING_LOCATION.append([current_node, current_func])
                            funcs_to_map.pop(0)
                            func_count += 1
                        else:
                            continue


def SingleMapping(path_obj):
    """
    First need to determine if path has enough resources for single mapping.
    """
    fused_path = PathObj.create_fusion_obj_list(path_obj.route)
    req_info = path_obj.REQ_INFO
    funcs_to_map = req_info[0].copy()  # ToDo need to be COPYING LISTS OTHERWISE WE ARE DIRECTLY REFERENCING THEM!
    requested_bandwidth = int(req_info[2])
    end_node = fused_path[-1]
    end_link = fused_path[-2]

    enough_bw = False
    all_mapped = False

    funcs_mapped = []
    func_count = 0

    for step in fused_path:
        if all_mapped and enough_bw:
            return True
        if type(step) == LinkObj:
            # print("Link ID: {} Src: {} Dest: {}".format(step.linkID, step.linkSrc, step.linkDest))
            # NOTE: In HvW Protocol if a link doesnt have enough BW the path fails
            check_bw = step.check_enough_resources(requested_bandwidth)
            if not check_bw:
                path_obj.state = POOR
                return False
            elif step.linkID == end_link.linkID:
                enough_bw = True
        else:
            if all_mapped:
                continue
            else:
                current_node = step  # First we must determine if mapping is even possible

                # if current_node.nodeID in AUTO_FAIL:
                #     path_obj.state = POOR
                #     return False
                if current_node.status == 'O':
                    # print("MAPPING ON NODE {} IS NOT POSSIBLE NODE IS OFFLINE".format(current_node.nodeID))
                    NodeObj.AUTO_FAIL.append(current_node.nodeID)
                    path_obj.state = POOR
                    return False
                elif current_node.status == 'R':
                    continue
                else:  # Next we need to determine if a node has enough resources for mapping and how many it can handle

                    if len(funcs_to_map) == 0:
                        all_mapped = True
                        continue
                    else:
                        current_func = funcs_to_map[0]
                        mappable = current_node.check_enough_resources(current_func)

                        if not mappable and step.nodeID == end_node.nodeID and len(funcs_to_map) > 0:
                            path_obj.state = POOR
                            return False
                        elif mappable:
                            funcs_mapped.append(current_func)
                            path_obj.MAPPING_LOCATION.append([current_node, current_func])
                            funcs_to_map.pop(0)
                            func_count += 1
                        else:
                            continue


def SingleMappingDemo(path_obj):
    route = path_obj.route

    for step in route:
        current_func = needed_funcs[-1]
        if step.has_enough_resources:
            continue # to next step
        else:
            fail_route