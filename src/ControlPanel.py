import os
# This script just controls globally used variables so I don't have to change them everywhere
# Resources
baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
outputFolder = os.path.join(baseFolder, "output")

# INPUT FILE PATHS

NodeInputData = os.path.join(resourcesFolder, "NodeInputData.csv")
LinkInputData = os.path.join(resourcesFolder, "LinkInputData.csv")
RequestInputData = os.path.join(resourcesFolder, "RequestInputData.txt")

# OUTPUT FILE PATHS

GLOBAL_OUTPUT_FILE_PATH_ONE = os.path.join(outputFolder, "PATH_ONE_REQUESTS_OUTPUT_MAX.csv")
GLOBAL_OUTPUT_FILE_PATH_TWO = os.path.join(outputFolder, "PATH_TWO_REQUESTS_OUTPUT_MAX.csv")

GLOBAL_NODE_RESOURCES = [1000, 1000, 1000]
GLOBAL_LINK_BANDWIDTH = 1000

GLOBAL_REQUEST_DELAY_THRESHOLD = 250.5
GlOBAL_FAILURE_THRESHOLD = 110