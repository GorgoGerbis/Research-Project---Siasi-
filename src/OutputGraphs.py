import os
import numpy as np
import matplotlib.pyplot as plt

all_fps = [r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_ONE_OUTPUT_DATA_25.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_TWO_OUTPUT_DATA_25.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_ONE_OUTPUT_DATA_50.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_TWO_OUTPUT_DATA_50.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_ONE_OUTPUT_DATA_75.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_TWO_OUTPUT_DATA_75.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_ONE_OUTPUT_DATA_100.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_TWO_OUTPUT_DATA_100.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_ONE_OUTPUT_DATA_200.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_TWO_OUTPUT_DATA_200.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_ONE_OUTPUT_DATA_300.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_TWO_OUTPUT_DATA_300.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_ONE_OUTPUT_DATA_500.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\MULTI_PATH_TWO_OUTPUT_DATA_500.csv",

           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_ONE_OUTPUT_DATA_25.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_TWO_OUTPUT_DATA_25.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_ONE_OUTPUT_DATA_50.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_TWO_OUTPUT_DATA_50.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_ONE_OUTPUT_DATA_75.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_TWO_OUTPUT_DATA_75.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_ONE_OUTPUT_DATA_100.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_TWO_OUTPUT_DATA_100.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_ONE_OUTPUT_DATA_200.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_TWO_OUTPUT_DATA_200.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_ONE_OUTPUT_DATA_300.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_TWO_OUTPUT_DATA_300.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_ONE_OUTPUT_DATA_500.csv",
           r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-\output\SINGLE_PATH_TWO_OUTPUT_DATA_500.csv"]

baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
outputFolder = os.path.join(baseFolder, "output")


def process_input_data(filePath, count):
    with open(filePath) as fp:
        count += 1
        name = "MULTI then SINGLE " + str(count)
        fp.readline()
        fp.readline()
        avg = fp.readline()
        averages = avg.split(',')
        avg_delay = averages[2]
        avg_cost = averages[3]
        avg_fail = averages[4]

        print("FILEPATH: {} DELAY: {} COST: {} FAIL: {}\n".format(name, avg_delay, avg_cost, avg_fail))
        fp.close()


def create_bar_graph(path_one_data, path_two_data):
    N = 7 # was 5 before figuring out what it does
    ind = np.arange(N)
    width = 0.35
    ax1 = plt.bar(ind, path_one_data, width, label='Conventional Scheme')
    ax2 = plt.bar(np.add(ind, width), path_two_data, width, label='Fault-Aware Scheme')
    plt.ylabel('Successful Requests')
    plt.title('Request success rates: Conventional mapping Vs. Fault-Aware mapping')

    plt.xticks(ind + width / 2, ('25 REQ', '50 REQ', '75 REQ', '100 REQ', '200 REQ', '300 REQ', '500 REQ'))
    plt.ylim([0, 100])
    plt.legend(loc='best')

    for bar in ax1:
        height = bar.get_height()
        plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{}%".format(height), ha='center')

    for bar in ax2:
        height = bar.get_height()
        plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{}%".format(height), ha='center')

    plt.show()


def create_bar_graph_delays(path_one_data, path_two_data):
    N = 7  # was 5 before figuring out what it does
    ind = np.arange(N)
    width = 0.35
    ax1 = plt.bar(ind, path_one_data, width, label='Conventional Scheme')
    exo = ind + width
    ax2 = plt.bar(exo, path_two_data, width, label='Fault-Aware Scheme')
    plt.ylabel('Average request delay')
    plt.title('Average request delay: Conventional mapping Vs. Fault-Aware mapping')

    plt.xticks(ind + width / 2, ('25 REQ', '50 REQ', '75 REQ', '100 REQ', '200 REQ', '300 REQ', '500 REQ'))
    plt.ylim([0, 15])
    plt.legend(loc='best')

    for bar in ax1:
        height = bar.get_height()
        plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{} ms".format(height), ha='center')

    for bar in ax2:
        height = bar.get_height()
        plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{} ms".format(height), ha='center')

    plt.show()


def create_bar_graph_costs(path_one_data, path_two_data):
    N = 7  # was 5 before figuring out what it does
    ind = np.arange(N)
    width = 0.35
    ax1 = plt.bar(ind, path_one_data, width, label='Conventional Scheme')
    ax2 = plt.bar(ind + width, path_two_data, width, label='Fault-Aware Scheme')
    plt.ylabel('Average request cost')
    plt.title('Average request cost: Conventional mapping Vs. Fault-Aware mapping')

    plt.xticks(ind + width / 2, ('25 REQ', '50 REQ', '75 REQ', '100 REQ', '200 REQ', '300 REQ', '500 REQ'))
    plt.ylim([0, 70])
    plt.legend(loc='best')

    for bar in ax1:
        height = bar.get_height()
        plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{} mb".format(height), ha='center')

    for bar in ax2:
        height = bar.get_height()
        plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{} mb".format(height), ha='center')

    plt.show()


if __name__ == '__main__':
    count = 0
    for f in all_fps:
        count += 1
        process_input_data(f, count)
    ################### Updated as of 12/16/2021 # numbers from datasets: 25, 50, 75, 100, 200, 300, 500 ##############################
    multi_pathOne_failure_percentages = [40, 56, 48, 52, 39, 26, 16.8]
    multi_pathTwo_failure_percentages = [40, 64, 60, 59, 65.5, 54, 38.2]

    multi_pathOne_delays = [11.53, 12.07, 11.96, 12.03, 11.74, 11.94, 11.60]
    multi_pathTwo_delays = [11.53, 12.34, 12.58, 12.38, 12.98, 13.17, 12.78]

    multi_pathOne_costs = [44, 44.64, 44.44, 45.61, 46.28, 47.69, 46.78]
    multi_pathTwo_costs = [44, 45.31, 47.0, 46.69, 50.72, 54.01, 54.42]

    count = sum(multi_pathOne_failure_percentages)
    cnt = sum(multi_pathTwo_failure_percentages)

    dst = sum(multi_pathOne_costs)
    d = sum(multi_pathTwo_costs)
    x = d + dst

    print("multi path one overall: " + str(count/700) + " SCORE: " + str(count))
    print("multi path two overall: " + str(cnt / 700) + " SCORE: " + str(cnt))

    print("MULTI MAPPING SCHEME AVERAGES: " + str(x / 14) + "TOTAL COST: " + str(x))
    print("multi path one cummulative avg. cost: " + str(dst / 7) + " TOTAL MB: " + str(dst))
    print("multi path two cummulative avg. cost: " + str(d / 7) + " SCORE: " + str(d))

    create_bar_graph(multi_pathOne_failure_percentages, multi_pathTwo_failure_percentages)
    create_bar_graph_delays(multi_pathOne_delays, multi_pathTwo_delays)
    create_bar_graph_costs(multi_pathOne_costs, multi_pathTwo_costs)
    ##################################################################################
    # 12/17/21
    # single_pathOne_failure_percentages = [40, 64, 54.6, 59, 62, 41, 23.6]
    # single_pathTwo_failure_percentages = [40, 68, 60, 62, 68.5, 57, 37.4]
    #
    # single_pathOne_delays = [8.07, 7.9, 8.03, 7.91, 8.23, 8.43, 8.15]
    # single_pathTwo_delays = [8.07, 7.89, 8.11, 8.05, 8.31, 8.81, 8.59]
    #
    # single_pathOne_costs = [37, 33.12, 34.51, 34.15, 36.53, 38.73, 37.2]
    # single_pathTwo_costs = [37, 33.52, 35.22, 34.83, 36.97, 40.78, 40.13]

    single_pathOne_failure_percentages = [40, 64, 54.6, 59, 62, 41, 23.6]
    single_pathTwo_failure_percentages = []

    single_pathOne_delays = [8.07, 7.9, 8.0, 7.91, 8.23, 8.43, 8.15]
    single_pathTwo_delays = []

    single_pathOne_costs = [37, 33.12, 34.51, 34.15, 36.53, 38.73, 37.2]
    single_pathTwo_costs = []

    count = sum(single_pathOne_failure_percentages)
    cnt = sum(single_pathTwo_failure_percentages)

    cst = sum(single_pathOne_costs)
    c = sum(single_pathTwo_costs)
    y = c + cst

    print("single path one overall: " + str(count / 700) + " SCORE: " + str(count))
    print("single path two overall: " + str(cnt / 700) + " SCORE: " + str(cnt))

    print("SINGLE MAPPING SCHEME AVERAGES: " + str(y / 14) + "TOTAL COST: " + str(y))
    print("single path one cummulative avg. cost: " + str(cst / 7) + " TOTAL MB: " + str(cst))
    print("single path two cummulative avg. cost: " + str(c / 7) + " SCORE: " + str(c))

    create_bar_graph(single_pathOne_failure_percentages, single_pathTwo_failure_percentages)
    create_bar_graph_delays(single_pathOne_delays, single_pathTwo_delays)
    create_bar_graph_costs(single_pathOne_costs, single_pathTwo_costs)
    ##################################################################################

    print("\n")
    print("Fault aware single(scheme 1) costs & multi(scheme 2) costs | Path Two Cummulative Avgs. = " + str((c + d)/14))
    print("NON Fault aware single(scheme 1) costs & multi(scheme 2) costs | Path Two Cummulative Avgs. = " + str((cst + dst)/14))