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

# INPUT FILE PATHS
NodeInputData = os.path.join(resourcesFolder, "NodeInputData.csv")
LinkInputData = os.path.join(resourcesFolder, "LinkInputData.csv")
RequestInputData = os.path.join(resourcesFolder, "RequestInputData_25.txt")

# OUTPUT FILE PATHS
GLOBAL_SINGLE_OUTPUT_FILE_PATH_ONE = os.path.join(outputFolder, "SINGLE_PATH_ONE_OUTPUT_DATA_25.csv")
GLOBAL_SINGLE_OUTPUT_FILE_PATH_TWO = os.path.join(outputFolder, "SINGLE_PATH_TWO_OUTPUT_DATA_25.csv")

GLOBAL_MULTI_OUTPUT_FILE_PATH_ONE = os.path.join(outputFolder, "MULTI_PATH_ONE_OUTPUT_DATA_25.csv")
GLOBAL_MULTI_OUTPUT_FILE_PATH_TWO = os.path.join(outputFolder, "MULTI_PATH_TWO_OUTPUT_DATA_25.csv")
############ Global file paths ###############


###### 1 == SINGLE MAPPING, 2 == MULTI-MAPPING
SINGLE_MAPPING = 1  # Mapping all/as many as possible on the first node in the route
MULTI_MAPPING = 2  # Mapping one function at a time on multiple different nodes

GLOBAL_PROTOCOL = 2

############## NEW TERMINAL STUFF #################
# @ToDo need to check that these randomly generated values are different each time they are called
GLOBAL_REQUEST_DELAY_THRESHOLD = 120
GlOBAL_FAILURE_THRESHOLD = 55.5

node_resources = [50, 64]  # [50, 64] <--> [CPU, MEMORY(RAM)]
link_bandwidth = 1000

# For CreateInputData script
CREATE_NUM_NODES = 7
CREATE_NUM_LINKS = 8
CREATE_NUM_REQUESTS = 25


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
