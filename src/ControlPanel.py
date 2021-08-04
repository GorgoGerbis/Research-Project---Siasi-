import os
# This script just controls globally used variables so I don't have to change them everywhere
# Resources
baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
outputFolder = os.path.join(baseFolder, "output")

# INPUT FILE PATHS

NodeInputData = os.path.join(resourcesFolder, "NodeInputData-TESTDATA-A-7-30-21.csv")
LinkInputData = os.path.join(resourcesFolder, "LinkInputData-TESTDATA-A-7-30-21.csv")
RequestInputData = os.path.join(resourcesFolder, "RequestInputData-TESTDATA-A-7-30-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-TEST-C-8-1-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-TEST-C-8-1-21.csv")
# RequestInputData = os.path.join(resourcesFolder, "RequestInputData-C-8-1-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-TEST-B-7-30-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-TEST-B-7-30-21.csv")
# RequestInputData = os.path.join(resourcesFolder, "RequestInputData-TEST-B-7-30-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-FUNC-TEST-C-7-28-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-FUNC-TEST-C-7-28-21.csv")
# RequestInputData = os.path.join(resourcesFolder, "RequestInputData-FUNC-TEST-C-7-28-21.txt")

# NodeInputData = os.path.join(resourcesFolder, "NodeInputData-EXSMALL-TEST-7-19-21.csv")
# LinkInputData = os.path.join(resourcesFolder, "LinkInputData-EXSMALL-TEST-7-19-21.csv")
# RequestInputData = os.path.join(resourcesFolder, "requests-EXSMALL-TEST-7-19-21.txt")

# OUTPUT FILE PATHS

GLOBAL_OUTPUT_FILE_PATH_ONE = os.path.join(outputFolder, "PATH_ONE_REQUESTS_OUTPUT_SMALL_TESTDATA_A.csv")
GLOBAL_OUTPUT_FILE_PATH_TWO = os.path.join(outputFolder, "PATH_TWO_REQUESTS_OUTPUT_SMALL_TESTDATA_A.csv")

# GLOBAL_OUTPUT_FILE_PATH_ONE = os.path.join(outputFolder, "PATH_ONE_REQUESTS_OUTPUT_C.csv")
# GLOBAL_OUTPUT_FILE_PATH_TWO = os.path.join(outputFolder, "PATH_TWO_REQUESTS_OUTPUT_C.csv")

# GLOBAL_OUTPUT_FILE_PATH_ONE = os.path.join(outputFolder, "REQUESTS_OUTPUT_A_NEW_7_26.csv")
# GLOBAL_OUTPUT_FILE_PATH_TWO = os.path.join(outputFolder, "REQUESTS_OUTPUT_A_WITH_FAULT_NEW_7_26.csv")

# REQUESTS_FILE = os.path.join(outputFolder, "REQUESTS_OUTPUT_FUNC_TEST_7_26.csv")
# REQUESTS_FILE_WITH = os.path.join(outputFolder, "REQUESTS_OUTPUT_FUNC_TEST_WITH_FAULT_7_26.csv")

# A_GLOBAL_NODE_RESOURCES = [200, 200, 200]
# A_GLOBAL_LINK_BANDWIDTH = 60
# A_GLOBAL_REQUEST_DELAY_THRESHOLD = 250.5
# A_GlOBAL_FAILURE_THRESHOLD = 55.5

# GLOBAL_NODE_RESOURCES = [80, 80, 80]
GLOBAL_NODE_RESOURCES = [10, 10, 10]
GLOBAL_LINK_BANDWIDTH = 25
GLOBAL_REQUEST_DELAY_THRESHOLD = 250.5
GlOBAL_FAILURE_THRESHOLD = 55.5

# C_GLOBAL_NODE_RESOURCES = [100, 100, 100]
# C_GLOBAL_LINK_BANDWIDTH = 35
# C_GLOBAL_REQUEST_DELAY_THRESHOLD = 250.5
# C_GlOBAL_FAILURE_THRESHOLD = 55.5