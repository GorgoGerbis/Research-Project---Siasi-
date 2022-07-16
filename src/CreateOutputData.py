from src.RequestObj import RequestObj
from src.CONSTANTS import GlOBAL_FAILURE_THRESHOLD, TOPOLOGY_NAME, DATASET, CREATE_NUM_NODES, CREATE_NUM_LINKS

from src.NodeObj import NodeObj

REQUEST_NEEDS_CALCULATING = 0
REQUEST_ONGOING = 1
REQUEST_DENIED = 2
REQUEST_APPROVED = 3


# def fail_unavailable_paths():
#     fails_output = []
#     failed_requests_data = set()
#     for req in RequestObj.STATIC_TOTAL_REQUEST_LIST:
#         if req.requestStatus[0] == REQUEST_APPROVED:
#             current_fail = req.PATH_ONE.FAILURE_PROBABILITY
#             current_fail_threshold = req.request_failure_threshold
#             if current_fail >= current_fail_threshold:
#                 fails_output.append(f"REQ:{req.requestID}, F% = {current_fail} > THRESHOLD = {current_fail_threshold}")
#                 req.requestStatus[0] = REQUEST_DENIED
#                 temp = (req.requestID, current_fail)
#                 failed_requests_data.add(temp)
#                 req.PATH_ONE = None
#
#     print(fails_output)
#     # return failed_requests_data


def process_and_separate_relevant_paths():  # FOR CONVENTIONAL SCHEMES ONLY
    request_output_strings = []     # ORDERED list of paths ready to be output...
    for req in RequestObj.STATIC_TOTAL_REQUEST_LIST:

        if req.requestStatus[0] == REQUEST_APPROVED:
            current_path = req.PATH_ONE
            current_fail_likelihood = req.PATH_ONE.FAILURE_PROBABILITY
            current_fail_threshold = req.request_failure_threshold

            # request_header = "REQUEST STATUS,REQUEST ID,PATH ID,FAILURE PROBABILITY,DELAY,COST,FUNCTIONS,PATH\n"

            if current_fail_likelihood > current_fail_threshold:    # PATHS THAT FAIL TO MEET FAILURE THRESHOLD REQUIREMENTS
                # print(f"FAILED REQUEST {current_path.pathID}, FAILURE LIKELIHOOD vs. THRESHOLD = {current_fail_likelihood} > {current_fail_threshold}\n")
                temp = "FAILED|,{}|,{}|,{}%|,{}|,{}|,{}|,{}|\n".format(req.requestID, current_path.pathID, current_path.FAILURE_PROBABILITY, current_path.DELAY, current_path.COST, req.requestedFunctions, current_path.route)
                request_output_strings.append(temp)

            else:   # TOTAL SUCCESS PATHS
                # print(f"PASSED REQUEST {current_path.pathID}, FAILURE LIKELIHOOD vs. THRESHOLD = {current_fail_likelihood} <= {current_fail_threshold}\n")
                temp = "APPROVED|,{}|,{}|,{}%|,{}|,{}|,{}|,{}|\n".format(req.requestID, current_path.pathID, current_path.FAILURE_PROBABILITY, current_path.DELAY, current_path.COST, req.requestedFunctions, current_path.route)
                request_output_strings.append(temp)

        else:   # PATHS THAT FAILED DUE TO DELAY, COST OR RESOURCE CONSTRAINTS
            temp = f"DENIED|,{req.requestID}|,NONE|,NONE%|,0|,0|,{req.requestedFunctions}|,src={req.source}|,dest={req.destination}|\n"
            request_output_strings.append(temp)

    for s in request_output_strings:
        print(s)

    return request_output_strings


def get_average_data_PATH_ONE(request_strings):
    total_approved = 0
    total_denied = 0
    total_mapped = 0

    fail_average = 0
    delay_average = 0
    cost_average = 0
    route_length_average = 0

    # @TODO Figure out if I should be calculating the average bandwidth and resources used per request or remaining per node....
    cpu = 0
    ram = 0
    bw = 0

    for s in request_strings:
        current_elements = s.split('|')
        status = current_elements[0]
        fail_prob = current_elements[3].strip(',')
        delay = current_elements[4].strip(',')
        cost = current_elements[5].strip(',')
        path_len = current_elements[7].count(',')

        if status == 'APPROVED':
            total_approved += 1
            total_mapped += 1
            fail_average += float(fail_prob.strip('%'))
            delay_average += float(delay)
            cost_average += float(cost)
            route_length_average += path_len
        if status == 'FAILED':
            total_denied += 1
            total_mapped += 1
            fail_average += float(fail_prob.strip('%'))
            delay_average += float(delay)
            cost_average += float(cost)
            route_length_average += path_len
        else:
            total_denied += 1

    delay_average = delay_average / total_mapped
    cost_average = cost_average / total_mapped
    fail_average = fail_average / total_mapped
    route_length_average = route_length_average / total_mapped

    return total_approved, total_denied, delay_average, cost_average, fail_average, route_length_average, [cpu, ram], bw


# def get_average_data_PATH_ONE(num_reqs, num_nodes, num_links):
#     # NEW LISTS
#     temp_req_list = []
#
#     delays = []
#     costs = []
#     fails = []
#     lens = []
#
#     total_approved = 0
#     total_denied = 0
#
#     delay = 0
#     cost = 0
#     fail = 0
#     lngth = 0
#
#     cpu = 0
#     ram = 0
#
#     bw = 0
#
#     for i in range(num_reqs):
#         i += 1
#         current_req = RequestObj.return_request(i)
#         temp_req_list.append(current_req)
#
#     for req in temp_req_list:
#         if req.requestStatus[0] == REQUEST_APPROVED:
#             total_approved += 1
#             obj = req.PATH_ONE
#             delays.append(obj.DELAY)
#             costs.append(obj.COST)
#             fails.append(obj.return_failure_probability())
#             lens.append(len(obj.route))
#         else:
#             total_denied += 1
#
#     for node in NodeObj.StaticNodeList:
#         n = node.nodeResources
#         cpu += n[0]
#         ram += n[1]
#
#     for lnk in NodeObj.StaticLinkList:
#         bw += lnk.linkBW
#
#     for d in delays:
#         delay += d
#
#     for c in costs:
#         cost += c
#
#     for f in fails:
#         fail += f
#
#     for l in lens:
#         lngth += l
#
#     delay_average = delay / total_approved
#     cost_average = cost / total_approved
#     fail_average = fail / total_approved
#     route_average = lngth / total_approved
#
#     cpu = cpu / num_nodes
#     ram = ram / num_nodes
#
#     bw = bw / num_links
#
#     return total_approved, total_denied, delay_average, cost_average, fail_average, route_average, [cpu, ram], bw


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


def output_file_PATH_ONE_S(FILE_NAME, num_reqs, num_nodes, num_links):
    # temp_reqs = []
    # fail_unavailable_paths()    # This will fail all paths that have a failed node in its route

    output_strings = process_and_separate_relevant_paths()  # LIST OF ALL REQUEST STRINGS AFTER BEING PROCESSED

    with open(FILE_NAME, 'w') as fp:
        main_header = f"TOPOLOGY={TOPOLOGY_NAME},DATASET={DATASET},TYPE=WITHOUT_FAULT_TOLERANCE,NODES={CREATE_NUM_NODES},LINKS={CREATE_NUM_LINKS},REQUESTS=250\n"
        average_header = "REQUEST PASSED, REQUESTS FAILED, AVERAGE REQUEST DELAY, AVERAGE REQUEST COST, AVERAGE FAILURE PROBABILITY, AVERAGE LENGTH OF PATHS, MEAN NODE [CPU, RAM], MEAN LINK BANDWIDTH\n"
        p, f, avd, avc, FAIL, route, resources, bw = get_average_data_PATH_ONE(output_strings)
        avg = "{},{},{},{},{}%,{},{},{}\n".format(p, f, avd, avc, FAIL, route, resources, bw)
        request_header = "REQUEST STATUS,REQUEST ID,PATH ID,FAILURE PROBABILITY,DELAY,COST,FUNCTIONS,PATH\n"
        fp.write(main_header)
        fp.write(average_header)
        fp.write(avg)
        fp.write(request_header)

        for req_str in output_strings:
            fp.write(req_str)

        # for i in range(num_reqs):
        #     i += 1
        #     current = RequestObj.return_request(i)
        #     temp_reqs.append(current)
        #
        # for req in temp_reqs:
        #     current_path = req.PATH_ONE
        #     if req.requestStatus[0] == REQUEST_APPROVED:
        #         fp.write("APPROVED|,{}|,{}|,{}%|,{}|,{}|,{}|,{}|\n".format(req.requestID, current_path.pathID, current_path.FAILURE_PROBABILITY, current_path.DELAY, current_path.COST, req.requestedFunctions, current_path.route))
        #     else:
        #         fp.write(f"DENIED|,{req.requestID}|,NONE|,NONE%|,0|,0|,{req.requestedFunctions}|,src={req.source}|,dest={req.destination}|\n")
    fp.close()
    print("CREATED CONVENTIONAL PATH ONE SINGLE-MAPPING OUTPUT FILES\n")


def output_file_PATH_ONE_M(FILE_NAME, num_reqs, num_nodes, num_links):
    # temp_reqs = []
    # fail_unavailable_paths() # This will fail all paths that have a failed node in its route

    output_strings = process_and_separate_relevant_paths()  # LIST OF ALL REQUEST STRINGS AFTER BEING PROCESSED

    with open(FILE_NAME, 'w') as fp:
        main_header = f"TOPOLOGY={TOPOLOGY_NAME},DATASET={DATASET},TYPE=WITHOUT_FAULT_TOLERANCE,NODES={CREATE_NUM_NODES},LINKS={CREATE_NUM_LINKS},REQUESTS=250\n"
        average_header = "REQUEST PASSED, REQUESTS FAILED, AVERAGE REQUEST DELAY, AVERAGE REQUEST COST, AVERAGE FAILURE PROBABILITY, AVERAGE LENGTH OF PATHS, MEAN NODE [CPU, RAM], MEAN LINK BANDWIDTH\n"
        p, f, avd, avc, FAIL, route, resources, bw = get_average_data_PATH_ONE(output_strings)
        avg = "{},{},{},{},{}%,{},{},{}\n".format(p, f, avd, avc, FAIL, route, resources, bw)
        request_header = "REQUEST STATUS,REQUEST ID,PATH ID,FAILURE PROBABILITY,DELAY,COST,FUNCTIONS,PATH\n"
        fp.write(main_header)
        fp.write(average_header)
        fp.write(avg)
        fp.write(request_header)

        for req_str in output_strings:
            fp.write(req_str)

        # for i in range(num_reqs):
        #     i += 1
        #     current = RequestObj.return_request(i)
        #     temp_reqs.append(current)
        #
        # for req in temp_reqs:
        #     current_path = req.PATH_ONE
        #     if req.requestStatus[0] == REQUEST_APPROVED:
        #         fp.write("APPROVED|,{}|,{}|,{}%|,{}|,{}|,{}|,{}|\n".format(req.requestID, current_path.pathID, current_path.FAILURE_PROBABILITY, current_path.DELAY, current_path.COST, req.requestedFunctions, current_path.route))
        #     else:
        #         fp.write(f"DENIED|,{req.requestID}|,NONE|,NONE%|,0|,0|,{req.requestedFunctions}|,src={req.source}|,dest={req.destination}|\n")

    fp.close()
    print("CREATED CONVENTIONAL PATH ONE MULTI-MAPPING OUTPUT FILES\n")


def output_file_PATH_TWO_S(FILE_NAME, num_reqs, num_nodes, num_links):
    temp_reqs = []

    with open(FILE_NAME, 'w') as fp:
        main_header = f"TOPOLOGY={TOPOLOGY_NAME},DATASET={DATASET},TYPE=WITH_FAULT_TOLERANCE,NODES={CREATE_NUM_NODES},LINKS={CREATE_NUM_LINKS},REQUESTS=250\n"
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
    fp.close()
    print("CREATED PATH TWO OUTPUT FILES\n")


def output_file_PATH_TWO_M(FILE_NAME, num_reqs, num_nodes, num_links):
    temp_reqs = []

    with open(FILE_NAME, 'w') as fp:
        main_header = f"TOPOLOGY={TOPOLOGY_NAME},DATASET={DATASET},TYPE=WITH_FAULT_TOLERANCE,NODES={CREATE_NUM_NODES},LINKS={CREATE_NUM_LINKS},REQUESTS=250\n"
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
    fp.close()
    print("CREATED PATH TWO OUTPUT FILES\n")