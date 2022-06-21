"""
@author: Jackson Walker

File holding all global and constant variables that would need to be adjusted/changed pre-runtime.

@ToDo should I just make this into a class so I dont have to constantly change imports or....?
"""
import os
import random

############ Global file paths ###############
# baseFolder = r"C:\Users\jacks\OneDrive\Desktop\Siasi Research\Research-Project---Siasi-" # <-- Fp for ws1
baseFolder = r"C:\Users\jacks\OneDrive\Desktop\Siasi Research\Research-Project---Siasi-"  # <-- Fp for ws0

resourcesFolder = os.path.join(baseFolder, "resources")
outputFolder = os.path.join(baseFolder, "output")


############## NEW TERMINAL STUFF #################
# @ToDo need to check that these randomly generated values are different each time they are called
GLOBAL_REQUEST_DELAY_THRESHOLD = 120
GlOBAL_FAILURE_THRESHOLD = 55.5

# @TODO YOU CAN NOT! EDIT THE CLASS RESOURCES HERE NEED TO DO IT IN PROCESSING DATA SCRIPT MANUALLY
node_resources = [50, 64]   # CAN NOT EDIT RESOURCES HERE NEED TO DO IT IN PROCESSING DATA  # [50, 64] <--> [CPU, MEMORY(RAM)]
link_bandwidth = 100   # CAN NOT EDIT RESOURCES HERE NEED TO DO IT IN PROCESSING DATA

# For CreateInputData script
CREATE_NUM_NODES = 50
CREATE_NUM_LINKS = 100
CREATE_NUM_REQUESTS = 250    # REMEMBER TO CHANGE THIS SO OUTPUT AND INPUT FILES MATCH!
CREATE_NUM_TERMINALS = 150  # NUM_TERMINALS = NUM_NODES x 3

# VERSION CONTROL
DATASET = 1
NETWORK_TOPOLOGY = 1

# INPUT FILE PATHS
NodeInputData = os.path.join(resourcesFolder, f"N{NETWORK_TOPOLOGY}_NodeInputData.csv")
LinkInputData = os.path.join(resourcesFolder, f"N{NETWORK_TOPOLOGY}_LinkInputData.csv")
RequestInputData = os.path.join(resourcesFolder, "D{}_RequestInputData_{}.txt".format(DATASET, CREATE_NUM_REQUESTS))

# OUTPUT FILE PATHS
GLOBAL_SINGLE_OUTPUT_FILE_PATH_ONE = os.path.join(outputFolder, "D{}N{}_SINGLE_PATH_ONE_OUTPUT_DATA_{}_RANDOM.csv".format(DATASET, NETWORK_TOPOLOGY, CREATE_NUM_REQUESTS))
GLOBAL_SINGLE_OUTPUT_FILE_PATH_TWO = os.path.join(outputFolder, "D{}N{}_SINGLE_PATH_TWO_OUTPUT_DATA_{}_RANDOM.csv".format(DATASET, NETWORK_TOPOLOGY, CREATE_NUM_REQUESTS))

GLOBAL_MULTI_OUTPUT_FILE_PATH_ONE = os.path.join(outputFolder, "D{}N{}_MULTI_PATH_ONE_OUTPUT_DATA_{}_RANDOM.csv".format(DATASET, NETWORK_TOPOLOGY, CREATE_NUM_REQUESTS))
GLOBAL_MULTI_OUTPUT_FILE_PATH_TWO = os.path.join(outputFolder, "D{}N{}_MULTI_PATH_TWO_OUTPUT_DATA_{}_RANDOM.csv".format(DATASET, NETWORK_TOPOLOGY, CREATE_NUM_REQUESTS))
############ Global file paths ###############

###### 1 == SINGLE MAPPING, 2 == MULTI-MAPPING
# Mapping one function at a time on multiple different nodes
SINGLE_MAPPING_PATH_ONE = 1
SINGLE_MAPPING_PATH_TWO = 2

# Mapping all/as many as possible on the first node in the route
MULTI_MAPPING_PATH_ONE = 3
MULTI_MAPPING_PATH_TWO = 4


GLOBAL_PROTOCOL = 1     # MOST IMPORTANT VARIABLE DETERMINES ACTUAL MAPPING SCHEME THAT WILL BE RUN
MAPPING_LOG_DATA = os.path.join(outputFolder, "D{}N{}_SCHEME_{}R_NETWORK_LOGS_{}.csv".format(DATASET, NETWORK_TOPOLOGY, GLOBAL_PROTOCOL, CREATE_NUM_REQUESTS))
AGGREGATE_DATASETS_AVERAGES = os.path.join(outputFolder, f"D{DATASET}N{NETWORK_TOPOLOGY}_AGGREGATE_DATASETS_AVERAGES_06_21_22.csv")


def MAPPING_LOG(request_info, resource_line, fpt):
    with open(MAPPING_LOG_DATA, fpt) as fp:
        fp.write('\n')
        fp.write(request_info)
        fp.write(resource_line)
        fp.write('\n')


def get_reqBW():  # @ToDo Maybe we should be adjusting this to match their num_funcs
    requestedBW = random.randint(5, 25)
    return requestedBW


def get_VNFs():
    num_VNFs = random.randint(1, 5)  # Random amount of functions
    return num_VNFs


def get_node_fail():  # @ToDo Need to come up with ideal failure solution
    node_fail = random.randint(1, 75) / 100
    return node_fail


def get_processing_delay():
    processing_delay = random.randint(1, 10) / 10  # <-- 1 ms
    return processing_delay


def get_link_fail():  # @ToDo Need to come up with ideal failure solution
    link_fail = random.randint(1, 100) / 100  # Dividing to make them decimals
    return link_fail


def get_edge_delay():
    edge_delay = random.randint(75, 300) / 100  # Dividing to make them decimals
    return edge_delay


def get_node_cost():
    node_cost = random.randint(5, 10) / 10
    return node_cost


def get_edge_cost():
    edge_cost = 1.5  # Based off of paper 2 averages
    return edge_cost
