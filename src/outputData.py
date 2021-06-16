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
# ToDo need to implement the output onto a csv file
REQUESTS_PASSED_FAILURE_PROBABILITY = os.path.join(outputFolder, "REQUESTS_PASSED_FAILURE_PROBABILITY.csv")
REQUESTS_FAILED_FAILURE_PROBABILITY = os.path.join(outputFolder, "REQUESTS_FAILED_FAILURE_PROBABILITY.csv")


def create_requests_failed(requests_failed):
    with open(REQUESTS_FAILED_FILE, 'w') as fp:
        heading = "Request ID;Source;Destination;Functions;BW;ALL FAILED\n"
        fp.write(heading)

        for i in range(len(requests_failed)-1):
            current_raw = requests_failed[i]
            fp.write("{}; {}; {}; {}; {}; {};\n".format(current_raw[0], current_raw[1], current_raw[2], current_raw[3], current_raw[4], current_raw[5]))


def create_requests_passed(requests_passed):
    with open(REQUESTS_PASSED_FILE, 'w') as fp:
        # Request ID: 9 Output: Path: ['5', '2'] Weight: 37927.867718402675
        heading = "Request ID;Source;Destination;Functions;Bandwidth;Path;Weight\n"
        fp.write(heading)

        for i in range(len(requests_passed)-1):
            current_raw = requests_passed[i]
            fp.write("{}; {}; {}; {}; {}; {};\n".format(current_raw[0], current_raw[1], current_raw[2], current_raw [3], current_raw[4], current_raw[5]))


def create_output(requests, requests_failed, requests_passed):
    # with open(REQUESTS_FILE, 'w') as fp:
    #     heading = ""
    #     fp.write(heading)
    #
    #     for i in range(len(requests)):
    #         current_raw = requests[i]
    #         print(current_raw)

    create_requests_failed(requests_failed)
    create_requests_passed(requests_passed)

#
# if __name__ == '__main__':
#     create_output()
