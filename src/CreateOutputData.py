import os
from src.Request import Request
from src.FuncObj import FuncObj
from src.PathObj import PathObj

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

REQUEST_NEEDS_CALCULATING = 0
REQUEST_ONGOING = 1
REQUEST_DENIED = 2
REQUEST_APPROVED = 3


def output_file():
    with open(REQUESTS_FILE, 'w') as fp:
        heading = "OUTPUT FILE TEMPLATE\n"
        fp.write(heading)

        for req in Request.STATIC_TOTAL_REQUEST_LIST:
            if req.requestStatus == REQUEST_APPROVED:
                fp.write("APPROVED,{}\n".format(req))
            else:
                fp.write("DENIED,{}\n".format(req))

# if __name__ == '__main__':
#     output_file(REQUESTS_FILE)