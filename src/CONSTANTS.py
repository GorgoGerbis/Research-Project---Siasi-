"""
@author: Jackson Walker

File holding all global and constant variables that would need to be adjusted/changed pre-runtime.

@ToDo should I just make this into a class so I dont have to constantly change imports or....?
"""
import os
import random

###### 1 == SINGLE MAPPING, 2 == MULTI-MAPPING
# Mapping one function at a time on multiple different nodes
SINGLE_MAPPING_PATH_ONE = 1
SINGLE_MAPPING_PATH_TWO = 2

# Mapping all/as many as possible on the first node in the route
MULTI_MAPPING_PATH_ONE = 3
MULTI_MAPPING_PATH_TWO = 4

GLOBAL_PROTOCOL = 1     # MOST IMPORTANT VARIABLE DETERMINES ACTUAL MAPPING SCHEME THAT WILL BE RUN

NETWORK_TOPOLOGY = 3    # VERSION CONTROL NETWORK ARCHITECTURE: 1-5
DATASET = 3     # REQUEST DATA SETS: 1-5

FAILURE_DISTRIBUTION = "RANDOM"
# FAILURE_DISTRIBUTION = "STATIC"

# CREATE_NUM_NODES = 0  # small:15, medium:50, large:100, # BONUS XL: 200  # BONUS MASS: 1000
# CREATE_NUM_LINKS = 0  # small:30, medium:100, large:200, # BONUS XL: 400 # BONUS MASS: 2000
# CREATE_NUM_TERMINALS = 0  # small:45, medium:150, large:300, # BONUS XL: 800 # BONUS MASS: 4000 # NUM_TERMINALS = NUM_NODES x 3
# MAX_LINKS_PER_TERMINAL = 0  # small:3, medium:3, large:3 # BONUS XL: 4 # BONUS MASS: 4
# MAX_LINKS_PER_NODE = 0  # small:4, medium:4, large:4 # BONUS XL: 4 # BONUS MASS: 4

if NETWORK_TOPOLOGY == 1:   # SMALL
    CREATE_NUM_NODES = 15
    CREATE_NUM_LINKS = 30
    CREATE_NUM_TERMINALS = 45
    MAX_LINKS_PER_TERMINAL = 3
    MAX_LINKS_PER_NODE = 4

if NETWORK_TOPOLOGY == 2:
    CREATE_NUM_NODES = 100
    CREATE_NUM_LINKS = 200
    CREATE_NUM_TERMINALS = 300
    MAX_LINKS_PER_TERMINAL = 3
    MAX_LINKS_PER_NODE = 4

    NUM_NODES_PER_LAYER = [10, 20, 40, 40]

if NETWORK_TOPOLOGY == 3:
    CREATE_NUM_NODES = 150
    CREATE_NUM_LINKS = 560
    CREATE_NUM_TERMINALS = 450
    MAX_LINKS_PER_TERMINAL = 3
    MAX_LINKS_PER_NODE = 4

    NUM_NODES_PER_LAYER = [10, 20, 40, 80]

if NETWORK_TOPOLOGY == 4:
    CREATE_NUM_NODES = 200
    CREATE_NUM_LINKS = 400
    CREATE_NUM_TERMINALS = 800
    MAX_LINKS_PER_TERMINAL = 4
    MAX_LINKS_PER_NODE = 4

if NETWORK_TOPOLOGY == 5:
    CREATE_NUM_NODES = 1000
    CREATE_NUM_LINKS = 2000
    CREATE_NUM_TERMINALS = 3000
    MAX_LINKS_PER_TERMINAL = 4
    MAX_LINKS_PER_NODE = 4

############## NEW TERMINAL STUFF #################
GLOBAL_REQUEST_DELAY_THRESHOLD = 120
GlOBAL_FAILURE_THRESHOLD = 55.5

# @TODO YOU CAN NOT! EDIT THE CLASS RESOURCES HERE NEED TO DO IT IN PROCESSING DATA SCRIPT MANUALLY
node_resources = [50, 64]   # CAN NOT EDIT RESOURCES HERE NEED TO DO IT IN PROCESSING DATA  # [50, 64] <--> [CPU, MEMORY(RAM)]
link_bandwidth = 100   # CAN NOT EDIT RESOURCES HERE NEED TO DO IT IN PROCESSING DATA
CREATE_NUM_REQUESTS = 250   # 250 # BONUS MASS: 500    # NUMBER OF NETWORK REQUESTS IS STATIC FOR ALL DATASETS AND TOPOLOGIES

############ Global file paths ###############
# baseFolder = r"C:\Users\jacks\OneDrive\Desktop\Siasi Research\Research-Project---Siasi-" # <-- Fp for ws1
baseFolder = r"C:\Users\jacks\OneDrive\Desktop\Siasi Research\Research-Project---Siasi-"  # <-- Fp for ws0

resourcesFolder = os.path.join(baseFolder, "resources")
topologyResourcesFolder = os.path.join(resourcesFolder, f"Topology_{NETWORK_TOPOLOGY}")
outputFolder = os.path.join(baseFolder, "output")
topologyOutputFolder = os.path.join(outputFolder, f"Topology_{NETWORK_TOPOLOGY}_output")

LOG_FOLDER = os.path.join(outputFolder, "Simulation Logs")
MAPPING_LOG_DATA = os.path.join(LOG_FOLDER, "N{}D{}_SCHEME_{}R_NETWORK_LOGS_{}.csv".format(NETWORK_TOPOLOGY, DATASET, GLOBAL_PROTOCOL, CREATE_NUM_REQUESTS))

# INPUT FILE PATHS
NodeInputData = os.path.join(topologyResourcesFolder, f"N{NETWORK_TOPOLOGY}_NodeInputData_{FAILURE_DISTRIBUTION}.csv")
LinkInputData = os.path.join(topologyResourcesFolder, f"N{NETWORK_TOPOLOGY}_LinkInputData_{FAILURE_DISTRIBUTION}.csv")
RequestInputData = os.path.join(topologyResourcesFolder, f"N{NETWORK_TOPOLOGY}D{DATASET}_RequestInputData_{CREATE_NUM_REQUESTS}_{FAILURE_DISTRIBUTION}.txt")

# OUTPUT FILE PATHS
GLOBAL_SINGLE_OUTPUT_FILE_PATH_ONE = os.path.join(topologyOutputFolder, f"N{NETWORK_TOPOLOGY}D{DATASET}_SINGLE_PATH_ONE_OUTPUT_DATA_{CREATE_NUM_REQUESTS}_{FAILURE_DISTRIBUTION}.csv")
GLOBAL_SINGLE_OUTPUT_FILE_PATH_TWO = os.path.join(topologyOutputFolder, f"N{NETWORK_TOPOLOGY}D{DATASET}_SINGLE_PATH_TWO_OUTPUT_DATA_{CREATE_NUM_REQUESTS}_{FAILURE_DISTRIBUTION}.csv")

GLOBAL_MULTI_OUTPUT_FILE_PATH_ONE = os.path.join(topologyOutputFolder, f"N{NETWORK_TOPOLOGY}D{DATASET}_MULTI_PATH_ONE_OUTPUT_DATA_{CREATE_NUM_REQUESTS}_{FAILURE_DISTRIBUTION}.csv")
GLOBAL_MULTI_OUTPUT_FILE_PATH_TWO = os.path.join(topologyOutputFolder, f"N{NETWORK_TOPOLOGY}D{DATASET}_MULTI_PATH_TWO_OUTPUT_DATA_{CREATE_NUM_REQUESTS}_{FAILURE_DISTRIBUTION}.csv")
############ Global file paths ###############


def MAPPING_LOG(request_info, resource_line, fpt):
    with open(MAPPING_LOG_DATA, fpt) as fp:
        fp.write('\n')
        fp.write(request_info)
        fp.write(resource_line)
        fp.write('\n')


def get_VNFs():
    num_VNFs = random.randint(1, 5)  # Random amount of functions
    return num_VNFs


def get_node_fail(region):  # @ToDo Need to come up with ideal failure solution
    if region == 1:
        node_fail = random.randint(30, 80) / 100

    elif region == 2:
        node_fail = random.randint(20, 50) / 100

    elif region == 3:
        node_fail = random.randint(15, 35) / 100

    elif region == 4:
        node_fail = random.randint(10, 30) / 100

    else:
        node_fail = random.randint(10, 80) / 100

    return node_fail*100


def get_link_fail(region):  # @ToDo Need to come up with ideal failure solution
    if region == 1:
        link_fail = random.randint(30, 80) / 100

    elif region == 2:
        link_fail = random.randint(20, 50) / 100

    elif region == 3:
        link_fail = random.randint(15, 35) / 100

    elif region == 4:
        link_fail = random.randint(10, 30) / 100

    else:
        link_fail = random.randint(10, 80) / 100

    return link_fail*100


def get_processing_delay(region):
    if region == 1:
        processing_delay = random.randint(1, 10) / 10  # <-- 1 ms

    elif region == 2:
        processing_delay = random.randint(1, 10) / 10  # <-- 1 ms

    elif region == 3:
        processing_delay = random.randint(1, 10) / 10  # <-- 1 ms

    elif region == 4:
        processing_delay = random.randint(1, 10) / 10  # <-- 1 ms

    else:
        processing_delay = random.randint(1, 10) / 10  # <-- 1 ms

    return processing_delay


def get_edge_delay(region):
    if region == 1:
        edge_delay = random.randint(75, 300) / 100  # Dividing to make them decimals

    elif region == 2:
        edge_delay = random.randint(75, 300) / 100  # Dividing to make them decimals

    elif region == 3:
        edge_delay = random.randint(75, 300) / 100  # Dividing to make them decimals

    elif region == 4:
        edge_delay = random.randint(75, 300) / 100  # Dividing to make them decimals

    else:
        edge_delay = random.randint(75, 300) / 100  # Dividing to make them decimals

    return edge_delay


def get_node_cost():
    node_cost = random.randint(5, 10) / 10
    return node_cost


def get_edge_cost():
    edge_cost = 1.5  # Based off of paper 2 averages
    return edge_cost
