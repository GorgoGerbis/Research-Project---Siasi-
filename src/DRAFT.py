def calculate_path_resources_PATH_ONE(path_obj, req_bw, req_vnfs):
    req_path_objs = PathObj.create_fusion_obj_list(path_obj.route)
    funcs_to_map = [VNFObj.retrieve_function_value(x) for x in req_vnfs]

    src = req_path_objs[0]
    dest = req_path_objs[-1]

    nodes = []  # list of nodes

    for obj in req_path_objs:
        if type(obj) == LinkObj:
            if not obj.check_enough_resources(req_bw):
                banner = "PATH{} LINK {} DID NOT HAVE ENOUGH BANDWIDTH!".format(path_obj.pathID, obj.linkID)
                print(banner)
                return False
        else:
            nodes.append((obj, []))

    for count, lst in enumerate(nodes): # Determines which nodes we can map
        node = lst[count]
        funcs = lst[count][1]
        for f in funcs_to_map:  # Fills up funcs with functions we can map to this node
            if node.can_map(f):
                funcs.append(f)

        if len(funcs) == 0: # If we cant map anything we remove it from the list
            nodes.pop(count)

    if len(nodes) == 0:
        banner = "PATH{} DID NOT HAVE ENOUGH RESOURCES TO MAP ANYWHERE PATH FAILS".format(path_obj.pathID)
        print(banner)
        return False
    else:
        for count, lst in enumerate(nodes):  # Now find out if we can map all the VNFs on this route
            node = lst[count]
            funcs = lst[count][1]
            for i, f in enumerate(funcs_to_map):  # Fills up funcs with functions we can map to this node
                if node.can_map(f):
                    funcs_to_map.pop(i)

        if len(funcs_to_map) == 0:
            return True
        else:
            banner = "PATH{} COULD NOT FIND LOCATION TO MAP {}".format(path_obj.pathID, funcs_to_map)
            print(banner)
            return False

def can_map(self, vnfObj): # <---- @ToDo made to replace check_mappable!
    cpu = vnfObj[0]
    ram = vnfObj[1]

    if self.compareCPU(cpu) and self.compareRAM(ram):
        return True
    else:
        return False


def optimal_mapping_multi(req_funcs, path):
    if we can map one at a time without ANY problems:
        return
    elif we can map multiple on one node and one at a time after:
    elif we need to resort to single mapping:

    1) first determine how many mappable in each location in the route
    2) prioritze one at a time
    3) then multiple