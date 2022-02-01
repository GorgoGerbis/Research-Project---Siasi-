import os
import numpy as np
import matplotlib.pyplot as plt

baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
outputFolder = os.path.join(baseFolder, "output")

single_pathOne_passed_avgs = [56.0, 57.2, 56.5, 53.8, 57.4, 39.8, 23.5]
single_pathTwo_passed_avgs = [60.0, 62.4, 60.7, 59.4, 63.1, 57.4, 35.1]
# single_pathOne_passed_avgs = [40.0, 40.85, 40.35, 38.42, 41.0, 28.45, 16.8, 14.87, 11.78]
# single_pathTwo_passed_avgs = [42.85, 44.57, 43.41, 42.42, 45.07, 41.04, 25.08, 22.77, 17.82]

multi_pathOne_passed_avgs = [52.0, 50.4, 49.8, 47.6, 37.0, 25.9, 15.0]
multi_pathTwo_passed_avgs = [59.2, 60.4, 59.4, 57.6, 60.7, 54.1, 36.5]
# multi_pathOne_passed_avgs = [37.14, 36.0, 35.6, 34.0, 26.42, 18.54, 10.77, 10.02, 09.42]
# multi_pathTwo_passed_avgs = [42.28, 43.14, 42.45, 41.14, 43.35, 38.66, 26.08, 23.67, 18.82]

single_pathOne_delays_avgs = []
single_pathTwo_delays_avgs = []

multi_pathOne_delays_avgs = []
multi_pathOne_delays_avgs = []

single_pathOne_costs_avgs = [32.65660173160173, 33.12028092874867, 35.304995973019224, 34.61352660111281, 36.775303952824025, 37.79436290103598]
single_pathTwo_costs_avgs = []

multi_pathOne_costs_avgs = []
multi_pathOne_costs_avgs = []


def create_bar_graph_COMBO(path_one_data_single, path_two_data_single, path_one_data_multi, path_two_data_multi):
    N = 7 # was 5 before figuring out what it does
    ind = np.arange(N)
    width = 0.2
    ax1 = plt.bar(ind, path_one_data_single, width, label='Single Conventional Scheme')
    ax2 = plt.bar(np.add(ind, width), path_two_data_single, width, label='Single Fault-Aware Scheme')

    ax3 = plt.bar(ind+0.4, path_one_data_multi, width, label='Multi Conventional Scheme')
    ax4 = plt.bar(np.add(ind+0.4, width), path_two_data_multi, width, label='Multi Fault-Aware Scheme')

    plt.ylabel('Successful Requests')
    plt.title('Success rates: Conventional mapping Vs. Fault-Aware mapping')

    plt.xticks(ind + width+0.1, ('25 REQ', '50 REQ', '75 REQ', '100 REQ', '200 REQ', '300 REQ', '500 REQ'))
    plt.ylim([0, 100])
    plt.legend(loc='best')

    for bar in ax1:
        height = bar.get_height()
        plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{}%".format(height), ha='center')

    for bar in ax2:
        height = bar.get_height()
        plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{}%".format(height), ha='center')

    for bar in ax3:
        height = bar.get_height()
        plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{}%".format(height), ha='center')

    for bar in ax4:
        height = bar.get_height()
        plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{}%".format(height), ha='center')

    plt.show()


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


if __name__ == '__main__':
    single_pathOne_passed_avgs = [40.0, 40.85, 40.35, 38.42, 41.0, 28.45, 16.8]
    single_pathTwo_passed_avgs = [42.85, 44.57, 43.41, 42.42, 45.07, 41.04, 25.08]

    multi_pathOne_passed_avgs = [37.14, 36.0, 35.6, 34.0, 26.42, 18.54, 10.77]
    multi_pathTwo_passed_avgs = [42.28, 43.14, 42.45, 41.14, 43.35, 38.66, 26.08]

    create_bar_graph_COMBO(single_pathOne_passed_avgs, single_pathTwo_passed_avgs, multi_pathOne_passed_avgs, multi_pathTwo_passed_avgs)