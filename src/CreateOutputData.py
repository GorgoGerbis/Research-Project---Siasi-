from src.Request import Request
from src.CONSTANTS import GLOBAL_OUTPUT_FILE_PATH_ONE
from src.CONSTANTS import GLOBAL_OUTPUT_FILE_PATH_TWO

#NEW FILE
from src.CONSTANTS import OUTPUT_SET_ONE_A
from src.CONSTANTS import OUTPUT_SET_ONE_B

from src.NodeObj import NodeObj

REQUEST_NEEDS_CALCULATING = 0
REQUEST_ONGOING = 1
REQUEST_DENIED = 2
REQUEST_APPROVED = 3

AUTO_FAIL = []# [5, 6, 13, 19]


#@Nvm it works as intended, Path one type paths will map on failed nodes and just be failed after while type two will avoid failed nodes completely.
def fail_unavailable_paths():
    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        if req.requestStatus[0] == REQUEST_APPROVED:
            current_route = req.PATH_ONE.route
            for node in current_route:
                if node in AUTO_FAIL:
                    req.requestStatus[0] = REQUEST_DENIED
                    req.PATH_ONE = None

########################################### NEW STUFF #################################################################


def NEW_get_average_data_PATH_ONE(num_range):
    # NEW LISTS
    temp_req_list = []

    delays = []
    costs = []
    fails = []
    lens = []

    total_approved = 0
    total_denied = 0

    delay = 0
    cost = 0
    fail = 0
    lngth = 0

    num_nodes = 20
    num_links = 30

    cpu = 0
    ram = 0
    pbs = 0

    bw = 0

    for i in range(num_range):
        i += 1
        current_req = Request.return_request(i)
        temp_req_list.append(current_req)

    for req in temp_req_list:
        if req.requestStatus[0] == REQUEST_APPROVED:
            total_approved += 1
            obj = req.PATH_ONE
            delays.append(obj.DELAY)
            costs.append(obj.COST)
            fails.append(obj.return_failure_probability())
            lens.append(len(obj.route))
        else:
            total_denied += 1

    for node in NodeObj.StaticNodeList:
        n = node.nodeResources
        cpu += n[0]
        ram += n[1]
        pbs += n[2]

    for lnk in NodeObj.StaticLinkList:
        bw += lnk.linkBW

    for d in delays:
        delay += d

    for c in costs:
        cost += c

    for f in fails:
        fail += f

    for l in lens:
        lngth += l

    delay_average = delay / total_approved
    cost_average = cost / total_approved
    fail_average = fail / total_approved
    route_average = lngth / total_approved

    cpu = cpu / num_nodes
    ram = ram / num_nodes
    pbs = pbs / num_nodes

    bw = bw / num_links

    return total_approved, total_denied, delay_average, cost_average, fail_average, route_average, [cpu, ram, pbs], bw


def NEW_get_average_data_PATH_TWO(num_range):
    # NEW LISTS
    temp_req_list = []

    delays = []
    costs = []
    fails = []
    lens = []

    total_approved = 0
    total_denied = 0

    delay = 0
    cost = 0
    fail = 0
    lngth = 0

    num_nodes = 20
    num_links = 30

    cpu = 0
    ram = 0
    pbs = 0

    bw = 0

    for i in range(num_range):
        i += 1
        current_req = Request.return_request(i)
        temp_req_list.append(current_req)

    for req in temp_req_list:
        if req.requestStatus[1] == REQUEST_APPROVED:
            total_approved += 1
            obj = req.PATH_TWO
            delays.append(obj.DELAY)
            costs.append(obj.COST)
            fails.append(obj.return_failure_probability())
            lens.append(len(obj.route))
        else:
            total_denied += 1

    for node in NodeObj.StaticNodeList:
        n = node.nodeResources
        cpu += n[0]
        ram += n[1]
        pbs += n[2]

    for lnk in NodeObj.StaticLinkList:
        bw += lnk.linkBW

    for d in delays:
        delay += d

    for c in costs:
        cost += c

    for f in fails:
        fail += f

    for l in lens:
        lngth += l

    delay_average = delay / total_approved
    cost_average = cost / total_approved
    fail_average = fail / total_approved
    route_average = lngth / total_approved

    cpu = cpu / num_nodes
    ram = ram / num_nodes
    pbs = pbs / num_nodes

    bw = bw / num_links

    # print("".format(total_approved, total_denied, delay_average, cost_average, fail_average, route_average, [cpu, ram, pbs], bw))
    return total_approved, total_denied, delay_average, cost_average, fail_average, route_average, [cpu, ram, pbs], bw


def NEW_output_file_PATH_ONE(FILE_NAME, num_range):
    temp_reqs = []

    fail_unavailable_paths() # This will fail all paths that have a failed node in its route
    with open(FILE_NAME, 'w') as fp:
        main_header = "DATASET=TEST_A,TYPE=WITHOUT_FAULT_TOLERANCE,NODES=42,LINKS=63,REQUESTS=100\n"
        average_header = "REQUEST PASSED, REQUESTS FAILED, AVERAGE REQUEST DELAY, AVERAGE REQUEST COST, AVERAGE FAILURE PROBABILITY, AVERAGE LENGTH OF PATHS, MEAN NODE [CPU, RAM, PBS], MEAN LINK BANDWIDTH\n"
        p, f, avd, avc, FAIL, route, resources, bw = NEW_get_average_data_PATH_ONE(num_range)
        avg = "{},{},{},{},{}%,{},{},{}\n".format(p, f, avd, avc, FAIL, route, resources, bw)
        request_header = "REQUEST STATUS,REQUEST ID,PATH ID,FAILURE PROBABILITY,DELAY,COST,FUNCTIONS,PATH\n"
        fp.write(main_header)
        fp.write(average_header)
        fp.write(avg)
        fp.write(request_header)

        for i in range(num_range):
            i += 1
            current = Request.return_request(i)
            temp_reqs.append(current)

        for req in temp_reqs:
            current_path = req.PATH_ONE
            if req.requestStatus[0] == REQUEST_APPROVED:
                fp.write("APPROVED,{},{},{}%,{},{},{},{}\n".format(req.requestID, current_path.pathID,
                                                                   current_path.FAILURE_PROBABILITY, current_path.DELAY,
                                                                   current_path.COST, req.requestedFunctions,
                                                                   current_path.route))
            else:
                fp.write("DENIED,{},NONE,NONE,0,0,{},src={}, dest={}\n".format(req.requestID, req.requestedFunctions,
                                                                               req.source, req.destination))


def NEW_output_file_PATH_TWO(FILE_NAME, num_range):
    temp_reqs = []

    with open(FILE_NAME, 'w') as fp:
        main_header = "DATASET=0-25,TYPE=WITH_FAULT_TOLERANCE,NODES=42,LINKS=63,REQUESTS=100\n"
        average_header = "REQUEST PASSED, REQUESTS FAILED, AVERAGE REQUEST DELAY, AVERAGE REQUEST COST, AVERAGE FAILURE PROBABILITY, AVERAGE LENGTH OF PATHS, MEAN NODE [CPU, RAM, PBS], MEAN LINK BANDWIDTH\n"
        p, f, avd, avc, FAIL, route, resources, bw = NEW_get_average_data_PATH_TWO(num_range)
        avg = "{},{},{},{},{}%,{},{},{}\n".format(p, f, avd, avc, FAIL, route, resources, bw)
        request_header = "REQUEST STATUS,REQUEST ID,PATH ID,FAILURE PROBABILITY,DELAY,COST,FUNCTIONS,PATH\n"
        fp.write(main_header)
        fp.write(average_header)
        fp.write(avg)
        fp.write(request_header)

        for i in range(num_range):
            i += 1
            current = Request.return_request(i)
            temp_reqs.append(current)

        for req in temp_reqs:
            current_path = req.PATH_TWO
            if req.requestStatus[1] == REQUEST_APPROVED:
                fp.write("APPROVED,{},{},{}%,{},{},{},{}\n".format(req.requestID, current_path.pathID, current_path.FAILURE_PROBABILITY, current_path.DELAY, current_path.COST, req.requestedFunctions, current_path.route))
            else:
                fp.write("DENIED,{},NONE,NONE,0,0,{},src={}, dest={}\n".format(req.requestID, req.requestedFunctions, req.source, req.destination))
