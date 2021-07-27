import os
import matplotlib.pyplot as plt
import numpy as np

from src.Request import Request
from src.FuncObj import FuncObj
from src.PathObj import PathObj

# ProcessPathing
import src.ProcessPathing
from src.FuncObj import FuncObj

baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
outputFolder = os.path.join(baseFolder, "output")

REQUESTS_FILE = os.path.join(outputFolder, "REQUESTS_OUTPUT_TEST_NEW_7_26.csv")
REQUESTS_FILE_WITH = os.path.join(outputFolder, "REQUESTS_OUTPUT_TEST_WITH_FAULT_NEW_7_26.csv")

REQUEST_NEEDS_CALCULATING = 0
REQUEST_ONGOING = 1
REQUEST_DENIED = 2
REQUEST_APPROVED = 3


def get_average_data_PATH_ONE():
    total_approved = 0
    total_denied = 0

    delay_average = 0
    cost_average = 0

    count = 0

    average_request_delay = []
    average_request_cost = []

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        if req.requestStatus[0] == 3:
            current_path = req.PATH_ONE
            total_approved += 1
            average_request_delay.append(current_path.DELAY)
            average_request_cost.append(current_path.COST)
            delay_average += current_path.DELAY
            cost_average += current_path.COST
            count += 1
        else:
            total_denied += 1
            continue

    cost_average = cost_average / count
    delay_average = delay_average / count

    return total_approved, total_denied, delay_average, cost_average


def get_average_data_PATH_TWO():
    total_approved = 0
    total_denied = 0

    delay_average = 0
    cost_average = 0
    average_request_delay = []
    average_request_cost = []

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        if req.requestStatus[1] == 3:
            current_path = req.PATH_TWO
            total_approved += 1
            average_request_delay.append(current_path.DELAY)
            average_request_cost.append(current_path.COST)
            delay_average += current_path.DELAY
            cost_average += current_path.COST
        else:
            total_denied += 1

    for delay in average_request_delay:
        delay_average += delay

    for cost in average_request_cost:
        cost_average += cost

    # cost_average = delay_average / len(average_request_cost)
    # delay_average = delay_average / len(average_request_delay)

    return total_approved, total_denied, delay_average, cost_average


def output_file_PATH_ONE():
    with open(REQUESTS_FILE, 'w') as fp:
        main_header = "DATASET=TEST_A,TYPE=WITHOUT_FAULT_TOLERANCE,NODES=42,LINKS=63,REQUESTS=100\n"
        average_header = "REQUEST PASSED, REQUESTS FAILED, AVERAGE REQUEST DELAY, AVERAGE REQUEST COST\n"
        p, f, avd, avc = get_average_data_PATH_ONE()
        avg = "{},{},{},{}\n".format(p, f, avd, avc)
        request_header = "REQUEST STATUS,REQUEST ID,PATH ID,FAILURE PROBABILITY,DELAY,COST,FUNCTIONS,PATH\n"
        fp.write(main_header)
        fp.write(average_header)
        fp.write(avg)
        fp.write(request_header)

        for req in Request.STATIC_TOTAL_REQUEST_LIST:
            current_path = req.PATH_ONE
            if req.requestStatus[0] == REQUEST_APPROVED:
                fp.write("APPROVED,{},{},{},{},{},{},{}\n".format(req.requestID, current_path.pathID, 0, current_path.DELAY, current_path.COST, req.requestedFunctions, current_path.route))
            else:
                fp.write("DENIED,{},NONE,NONE,0,0,{},NONE\n".format(req.requestID, req.requestedFunctions))


def output_file_PATH_TWO():
    with open(REQUESTS_FILE_WITH, 'w') as fp:
        main_header = "DATASET=TEST_A,TYPE=WITH_FAULT_TOLERANCE,NODES=42,LINKS=63,REQUESTS=100\n"
        average_header = "REQUEST PASSED, REQUESTS FAILED, AVERAGE REQUEST DELAY, AVERAGE REQUEST COST\n"
        p, f, avd, avc = get_average_data_PATH_TWO()
        avg = "{},{},{},{}\n".format(p, f, avd, avc)
        request_header = "REQUEST STATUS,REQUEST ID,PATH ID,FAILURE PROBABILITY,DELAY,COST,FUNCTIONS,PATH\n"
        fp.write(main_header)
        fp.write(average_header)
        fp.write(avg)
        fp.write(request_header)

        for req in Request.STATIC_TOTAL_REQUEST_LIST:
            current_path = req.PATH_TWO
            if req.requestStatus[1] == REQUEST_APPROVED:
                fp.write("APPROVED,{},{},{},{},{},{},{}\n".format(req.requestID, current_path.pathID, current_path.FAILURE_PROBABILITY, current_path.DELAY, current_path.COST, req.requestedFunctions, current_path.route))
            else:
                fp.write("DENIED,{},NONE,NONE,0,0,{},NONE\n".format(req.requestID, req.requestedFunctions))
