import os
from src.Request import Request
from src.FuncObj import FuncObj

# ProcessPathing
import src.ProcessPathing
from src.FuncObj import FuncObj

baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
outputFolder = os.path.join(baseFolder, "output")

REQUESTS_FILE = os.path.join(outputFolder, "REQUESTS.csv")
REQUESTS_FAILED_FILE = os.path.join(outputFolder, "REQUESTS_FAILED.csv")
REQUESTS_PASSED_FILE = os.path.join(outputFolder, "REQUESTS_PASSED.csv")
REQUESTS_PASSED_FAILURE_PROBABILITY = os.path.join(outputFolder, "REQUESTS_PASSED_FAILURE_PROBABILITY.csv")
REQUESTS_FAILED_FAILURE_PROBABILITY = os.path.join(outputFolder, "REQUESTS_FAILED_FAILURE_PROBABILITY.csv")

"""
REQUESTS FILE EX:

REQUESTID; REQUEST_
"""