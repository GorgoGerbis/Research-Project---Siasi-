import os
from src.Request import Request
from src.FuncObj import FuncObj
from src.Graph_Class import Graph

# ProcessPathing
import src.ProcessPathing
from src.FuncObj import FuncObj

baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
outputFolder = os.path.join(baseFolder, "output")

REQUESTS_FAILED_FILE = os.path.join(outputFolder, "REQUESTS_FAILED.csv")
REQUESTS_PASSED_FILE = os.path.join(outputFolder, "REQUESTS_PASSED.csv")
REQUESTS_FILE = os.path.join(outputFolder, "REQUESTS.csv")


def create_requests_failed(requests_failed):
    with open(REQUESTS_FAILED_FILE, 'w') as fp:
        heading = "Request ID;Path;Weight;\n"
        fp.write(heading)

        for i in range(len(requests_failed)):
            current_raw = requests_failed[i].split()
            print(current_raw)


def create_requests_passed(requests_passed):
    with open(REQUESTS_PASSED_FILE, 'w') as fp:
        # Request ID: 9 Output: Path: ['5', '2'] Weight: 37927.867718402675
        heading = "Request ID;Path;Weight;\n"
        fp.write(heading)

        for i in range(len(requests_passed)):
            current_raw = requests_passed[i].split()
            print(current_raw)


def create_output(requests, requests_passed, requests_failed):
    with open(REQUESTS_FILE, 'w') as fp:
        heading = ""
        fp.write(heading)

        for i in range(len(requests)):
            current_raw = requests[i].split()
            print(current_raw)

    print("created REQUESTS.csv")
    create_requests_failed(requests_failed)
    create_requests_passed(requests_passed)

    return

#
# if __name__ == '__main__':
#     create_output()
