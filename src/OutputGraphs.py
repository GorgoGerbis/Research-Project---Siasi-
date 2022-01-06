import os
import numpy as np
import matplotlib.pyplot as plt

baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
outputFolder = os.path.join(baseFolder, "output")

single_pathOne_passed_avgs = [40.0, 40.85, 40.35, 38.42, 41.0, 28.45, 16.8]
single_pathTwo_passed_avgs = [42.85, 44.57, 43.41, 42.42, 45.07, 41.04, 25.08]

multi_pathOne_passed_avgs = [37.14, 36.0, 35.6, 34.0, 26.42, 18.54, 10.77]
multi_pathTwo_passed_avgs = [42.28, 43.14, 42.45, 41.14, 43.35, 38.66, 26.08]


def create_bar_graph_SINGLE(path_one_data, path_two_data):
    N = 7 # was 5 before figuring out what it does
    ind = np.arange(N)
    width = 0.35
    ax1 = plt.bar(ind, path_one_data, width, label='Conventional Scheme')
    ax2 = plt.bar(np.add(ind, width), path_two_data, width, label='Fault-Aware Scheme')
    plt.ylabel('Successful Requests')
    plt.title('Single-Mapping success rates: Conventional mapping Vs. Fault-Aware mapping')

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


def create_bar_graph_MULTI(path_one_data, path_two_data):
    N = 7 # was 5 before figuring out what it does
    ind = np.arange(N)
    width = 0.35
    ax1 = plt.bar(ind, path_one_data, width, label='Conventional Scheme')
    ax2 = plt.bar(np.add(ind, width), path_two_data, width, label='Fault-Aware Scheme')
    plt.ylabel('Successful Requests')
    plt.title('Multi-Mapping success rates: Conventional mapping Vs. Fault-Aware mapping')

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


def create_line_graph_SINGLE(path_one_data, path_two_data):
    plt.title("Single-Mapping average requests passed")
    plt.xlabel("Number of requests")
    plt.ylabel("Average percent passed")

    N = 7
    y1 = path_one_data
    y2 = path_two_data

    ind = np.arange(N)
    width = 0.35
    plt.xticks(ind + width / 2, ('25 REQ', '50 REQ', '75 REQ', '100 REQ', '200 REQ', '300 REQ', '500 REQ'))
    plt.plot(ind + width / 2, path_one_data)
    plt.legend()

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
    single_pathOne_passed_avgs = [40.0, 40.85, 40.35, 38.42, 41.0, 28.45, 16.8]
    single_pathTwo_passed_avgs = [42.85, 44.57, 43.41, 42.42, 45.07, 41.04, 25.08]

    multi_pathOne_passed_avgs = [37.14, 36.0, 35.6, 34.0, 26.42, 18.54, 10.77]
    multi_pathTwo_passed_avgs = [42.28, 43.14, 42.45, 41.14, 43.35, 38.66, 26.08]

    # create_bar_graph_SINGLE(single_pathOne_passed_avgs, single_pathTwo_passed_avgs)
    # create_bar_graph_MULTI(multi_pathOne_passed_avgs, multi_pathTwo_passed_avgs)

    create_line_graph_SINGLE(single_pathOne_passed_avgs, single_pathTwo_passed_avgs)