import os
# This script just controls globally used variables so I don't have to change them everywhere
# Resources
# baseFolder = r"C:\Users\jacks\OneDrive\Desktop\Siasi Research\Research-Project---Siasi-"
baseFolder = r"C:\Users\jacks\OneDrive\Desktop\Siasi Research\Research-Project---Siasi-"

resourcesFolder = os.path.join(baseFolder, "resources")
outputFolder = os.path.join(baseFolder, "output")


SINGLE_MAPPING = 1  # Mapping all/as many as possible on the first node in the route
MULTI_MAPPING = 2   # Mapping one function at a time on multiple different nodes

# INPUT FILE PATHS

NodeInputData = os.path.join(resourcesFolder, "NodeInputData.csv")
LinkInputData = os.path.join(resourcesFolder, "LinkInputData.csv")
RequestInputData = os.path.join(resourcesFolder, "RequestInputData.txt")

# OUTPUT FILE PATHS

GLOBAL_OUTPUT_FILE_PATH_ONE = os.path.join(outputFolder, "SINGLE_PATH_ONE_OUTPUT_DATA_25.csv")
GLOBAL_OUTPUT_FILE_PATH_TWO = os.path.join(outputFolder, "SINGLE_PATH_TWO_OUTPUT_DATA_25.csv")

# GLOBAL_OUTPUT_FILE_PATH_ONE = os.path.join(outputFolder, "MULTI_PATH_ONE_OUTPUT_DATA_25.csv")
# GLOBAL_OUTPUT_FILE_PATH_TWO = os.path.join(outputFolder, "MULTI_PATH_TWO_OUTPUT_DATA_25.csv")

######### NEW STUFF ################
# OUTPUT_SET_ONE_A = os.path.join(outputFolder, "NEW_SINGLE_PATH_ONE_OUTPUT_DATA_25.csv")
# OUTPUT_SET_ONE_B = os.path.join(outputFolder, "NEW_SINGLE_PATH_TWO_OUTPUT_DATA_25.csv")
####################################

# WILL DELETE THIS METHOD LATER

GLOBAL_NODE_RESOURCES = [50, 64]
GLOBAL_LINK_BANDWIDTH = 1000

GLOBAL_REQUEST_DELAY_THRESHOLD = 120.5
GlOBAL_FAILURE_THRESHOLD = 55.5
GLOBAL_FAILURE_RATE = 0.15

###### 1 == SINGLE MAPPING, 2 == MULTI-MAPPING
GLOBAL_PROTOCOL = 1

############## NEW TERMINAL STUFF #################
INITIAL_TERMINAL_RESOURCES = 100