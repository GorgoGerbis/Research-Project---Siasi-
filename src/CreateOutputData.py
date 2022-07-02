from src.RequestObj import RequestObj
from src.CONSTANTS import GlOBAL_FAILURE_THRESHOLD

from src.NodeObj import NodeObj

REQUEST_NEEDS_CALCULATING = 0
REQUEST_ONGOING = 1
REQUEST_DENIED = 2
REQUEST_APPROVED = 3


def fail_unavailable_paths():
    fails_output = []
    failed_requests_data = set()
    for req in RequestObj.STATIC_TOTAL_REQUEST_LIST:
        if req.requestStatus[0] == REQUEST_APPROVED:
            current_fail = req.PATH_ONE.FAILURE_PROBABILITY
            current_fail_threshold = req.request_failure_threshold
            if current_fail >= current_fail_threshold:
                fails_output.append(f"REQ:{req.requestID}, F% = {current_fail} > THRESHOLD = {current_fail_threshold}")
                req.requestStatus[0] = REQUEST_DENIED
                temp = (req.requestID, current_fail)
                failed_requests_data.add(temp)
                req.PATH_ONE = None

    print(fails_output)
    return failed_requests_data


def get_average_data_PATH_ONE(num_reqs, num_nodes, num_links):
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

    cpu = 0
    ram = 0

    bw = 0

    for i in range(num_reqs):
        i += 1
        current_req = RequestObj.return_request(i)
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

    bw = bw / num_links

    return total_approved, total_denied, delay_average, cost_average, fail_average, route_average, [cpu, ram], bw


def get_average_data_PATH_TWO(num_reqs, num_nodes, num_links):
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

    cpu = 0
    ram = 0

    bw = 0

    for i in range(num_reqs):
        i += 1
        current_req = RequestObj.return_request(i)
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

    bw = bw / num_links

    # print("".format(total_approved, total_denied, delay_average, cost_average, fail_average, route_average, [cpu, ram, pbs], bw))
    return total_approved, total_denied, delay_average, cost_average, fail_average, route_average, [cpu, ram], bw


def output_file_PATH_ONE(FILE_NAME, num_reqs, num_nodes, num_links):
    temp_reqs = []

    failed_requests_data = fail_unavailable_paths() # This will fail all paths that have a failed node in its route
    with open(FILE_NAME, 'w') as fp:
        main_header = "DATASET=TINY,TYPE=WITHOUT_FAULT_TOLERANCE,NODES=42,LINKS=63,REQUESTS=100\n"
        average_header = "REQUEST PASSED, REQUESTS FAILED, AVERAGE REQUEST DELAY, AVERAGE REQUEST COST, AVERAGE FAILURE PROBABILITY, AVERAGE LENGTH OF PATHS, MEAN NODE [CPU, RAM], MEAN LINK BANDWIDTH\n"
        p, f, avd, avc, FAIL, route, resources, bw = get_average_data_PATH_ONE(num_reqs, num_nodes, num_links)
        avg = "{},{},{},{},{}%,{},{},{}\n".format(p, f, avd, avc, FAIL, route, resources, bw)
        request_header = "REQUEST STATUS,REQUEST ID,PATH ID,FAILURE PROBABILITY,DELAY,COST,FUNCTIONS,PATH\n"
        fp.write(main_header)
        fp.write(average_header)
        fp.write(avg)
        fp.write(request_header)

        for i in range(num_reqs):
            i += 1
            current = RequestObj.return_request(i)
            temp_reqs.append(current)

        for req in temp_reqs:
            current_path = req.PATH_ONE
            if req.requestStatus[0] == REQUEST_APPROVED:
                fp.write("APPROVED|,{}|,{}|,{}%|,{}|,{}|,{}|,{}|\n".format(req.requestID, current_path.pathID, current_path.FAILURE_PROBABILITY, current_path.DELAY, current_path.COST, req.requestedFunctions, current_path.route))
            else:
                fp.write(f"DENIED|,{req.requestID}|,NONE|,NONE%|,0|,0|,{req.requestedFunctions}|,src={req.source}|,dest={req.destination}|\n")
                # for t in failed_requests_data:
                #     if t[0] == i:
                #         fp.write(f"DENIED|,{req.requestID}|,NONE|,{t[1]}%|,0|,0|,{req.requestedFunctions}|,src={req.source}|,dest={req.destination}|\n")


def output_file_PATH_TWO(FILE_NAME, num_reqs, num_nodes, num_links):
    temp_reqs = []

    with open(FILE_NAME, 'w') as fp:
        main_header = "DATASET=TINY,TYPE=WITH_FAULT_TOLERANCE,NODES=42,LINKS=63,REQUESTS=100\n"
        average_header = "REQUEST PASSED, REQUESTS FAILED, AVERAGE REQUEST DELAY, AVERAGE REQUEST COST, AVERAGE FAILURE PROBABILITY, AVERAGE LENGTH OF PATHS, MEAN NODE [CPU, RAM], MEAN LINK BANDWIDTH\n"
        p, f, avd, avc, FAIL, route, resources, bw = get_average_data_PATH_TWO(num_reqs, num_nodes, num_links)
        avg = "{},{},{},{},{}%,{},{},{}\n".format(p, f, avd, avc, FAIL, route, resources, bw)
        request_header = "REQUEST STATUS,REQUEST ID,PATH ID,FAILURE PROBABILITY,DELAY,COST,FUNCTIONS,PATH\n"
        fp.write(main_header)
        fp.write(average_header)
        fp.write(avg)
        fp.write(request_header)

        for i in range(num_reqs):
            i += 1
            current = RequestObj.return_request(i)
            temp_reqs.append(current)

        for req in temp_reqs:
            current_path = req.PATH_TWO
            if req.requestStatus[1] == REQUEST_APPROVED:
                fp.write("APPROVED|,{}|,{}|,{}%|,{}|,{}|,{}|,{}|\n".format(req.requestID, current_path.pathID, current_path.FAILURE_PROBABILITY, current_path.DELAY, current_path.COST, req.requestedFunctions, current_path.route))
            else:
                fp.write(f"DENIED|,{req.requestID}|,NONE|,NONE%|,0|,0|,{req.requestedFunctions}|,src={req.source}|,dest={req.destination}|\n")