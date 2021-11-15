import os
# This script just controls globally used variables so I don't have to change them everywhere
# Resources
baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
outputFolder = os.path.join(baseFolder, "output")

# INPUT FILE PATHS

NodeInputData = os.path.join(resourcesFolder, "NodeInputData.csv")
LinkInputData = os.path.join(resourcesFolder, "LinkInputData.csv")
RequestInputData = os.path.join(resourcesFolder, "RequestInputData_75.txt")

# OUTPUT FILE PATHS

GLOBAL_OUTPUT_FILE_PATH_ONE = os.path.join(outputFolder, "PATH_ONE_OUTPUT_DATA_75.csv")
GLOBAL_OUTPUT_FILE_PATH_TWO = os.path.join(outputFolder, "PATH_TWO_OUTPUT_DATA_75.csv")

# WILL DELETE THIS METHOD LATER

GLOBAL_NODE_RESOURCES = [100, 100, 100]
GLOBAL_LINK_BANDWIDTH = 1000 # 60

GLOBAL_REQUEST_DELAY_THRESHOLD = 120.5
GlOBAL_FAILURE_THRESHOLD = 55.5
GLOBAL_FAILURE_RATE = 0.15


def INCREASE_FAILURE_RATE(r):
    r += 0.1
