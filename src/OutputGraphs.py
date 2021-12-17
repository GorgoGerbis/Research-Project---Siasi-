import os
import numpy as np
import matplotlib.pyplot as plt

baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
outputFolder = os.path.join(baseFolder, "output")


def process_input_data(filePath):
    with open(filePath) as fp:
        fp.readline()
        fp.readline()
        avg = fp.readline()
        averages = avg.split(',')
        for cnt, line in enumerate(fp):
            print("Line {}: {}".format(cnt, line))
            currentElements = line.split(';')


def create_bar_graph(path_one_data, path_two_data):
    N = 7 # was 5 before figuring out what it does
    ind = np.arange(N)
    width = 0.35
    ax1 = plt.bar(ind, path_one_data, width, label='Conventional Scheme')
    ax2 = plt.bar(ind + width, path_two_data, width, label='Fault-Aware Scheme')
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
    ax2 = plt.bar(ind + width, path_two_data, width, label='Fault-Aware Scheme')
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

    ################### Updated as of 12/16/2021 # numbers from datasets: 25, 50, 75, 100, 200, 300, 500 ##############################
    multi_pathOne_failure_percentages = [40, 56, 48, 52, 39, 26, 16.8]
    multi_pathTwo_failure_percentages = [40, 64, 60, 59, 65.5, 54, 38.2]

    multi_pathOne_delays = [11.53, 12.07, 11.96, 12.03, 11.74, 11.94, 11.60]
    multi_pathTwo_delays = [11.53, 12.34, 12.58, 12.38, 12.98, 13.17, 12.78]

    multi_pathOne_costs = [44, 44.64, 44.44, 45.61, 46.28, 47.69, 46.78]
    multi_pathTwo_costs = [44, 45.31, 47.0, 46.69, 50.72, 54.01, 54.42]

    create_bar_graph(multi_pathOne_failure_percentages, multi_pathTwo_failure_percentages)
    create_bar_graph_delays(multi_pathOne_delays, multi_pathTwo_delays)
    create_bar_graph_costs(multi_pathOne_costs, multi_pathTwo_costs)
    ##################################################################################
    single_pathOne_failure_percentages = [40, 64, 54.6, 59, 62, 41, 23.6]
    single_pathTwo_failure_percentages = [40, 68, 60, 62, 68.5, 57, 37.4]

    single_pathOne_delays = [8.07, 7.9, 8.03, 7.91, 8.23, 8.43, 8.15]
    single_pathTwo_delays = [8.07, 7.89, 8.11, 8.05, 8.31, 8.81, 8.59]

    single_pathOne_costs = [37, 33.12, 34.51, 34.15, 36.53, 38.73, 37.2]
    single_pathTwo_costs = [37, 33.52, 35.22, 34.83, 36.97, 40.78, 40.13]

    create_bar_graph(single_pathOne_failure_percentages, single_pathTwo_failure_percentages)
    create_bar_graph_delays(single_pathOne_delays, single_pathTwo_delays)
    create_bar_graph_costs(single_pathOne_costs, single_pathTwo_costs)
    ##################################################################################