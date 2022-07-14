import numpy as np
import os
from matplotlib.ticker import FormatStrFormatter

from src import CONSTANTS
from src.CONSTANTS import GLOBAL_SINGLE_OUTPUT_FILE_PATH_ONE, GLOBAL_SINGLE_OUTPUT_FILE_PATH_TWO, topologyOutputFolder, \
    FAILURE_DISTRIBUTION
from src.CONSTANTS import GLOBAL_MULTI_OUTPUT_FILE_PATH_ONE, GLOBAL_MULTI_OUTPUT_FILE_PATH_TWO
from src.CONSTANTS import outputFolder
from src.CONSTANTS import DATASET, NETWORK_TOPOLOGY, CREATE_NUM_REQUESTS
import matplotlib.pyplot as plt


def gather_all_data_averages(network_topology):
    universal_success_so = []
    universal_success_st = []
    universal_success_mo = []
    universal_success_mt = []

    universal_fails_so = []
    universal_fails_st = []
    universal_fails_mo = []
    universal_fails_mt = []

    universal_delays_so = []
    universal_delays_st = []
    universal_delays_mo = []
    universal_delays_mt = []

    universal_costs_so = []
    universal_costs_st = []
    universal_costs_mo = []
    universal_costs_mt = []

    global_success_so = []
    global_success_st = []
    global_success_mo = []
    global_success_mt = []

    global_fails_so = []
    global_fails_st = []
    global_fails_mo = []
    global_fails_mt = []

    global_delays_so = []
    global_delays_st = []
    global_delays_mo = []
    global_delays_mt = []

    global_costs_so = []
    global_costs_st = []
    global_costs_mo = []
    global_costs_mt = []

    if NETWORK_TOPOLOGY == 1:
        top_name = "SMALL"
    if NETWORK_TOPOLOGY == 2:
        top_name = "MEDIUM"
    if NETWORK_TOPOLOGY == 3:
        top_name = "LARGE"
    if NETWORK_TOPOLOGY == 4:
        top_name = "EX-LARGE"
    if NETWORK_TOPOLOGY == 5:
        top_name = "MASSIVE"

    start = 1
    stop = 5

    for ds in range(start, stop+1):
        so_passed, so_fails, so_delays, so_costs = gather_data(os.path.join(topologyOutputFolder, f"N{network_topology}D{ds}_SINGLE_PATH_ONE_OUTPUT_DATA_{CREATE_NUM_REQUESTS}_{FAILURE_DISTRIBUTION}.csv"))
        st_passed, st_fails, st_delays, st_costs = gather_data(os.path.join(topologyOutputFolder, f"N{network_topology}D{ds}_SINGLE_PATH_TWO_OUTPUT_DATA_{CREATE_NUM_REQUESTS}_{FAILURE_DISTRIBUTION}.csv"))
        mo_passed, mo_fails, mo_delays, mo_costs = gather_data(os.path.join(topologyOutputFolder, f"N{network_topology}D{ds}_MULTI_PATH_ONE_OUTPUT_DATA_{CREATE_NUM_REQUESTS}_{FAILURE_DISTRIBUTION}.csv"))
        mt_passed, mt_fails, mt_delays, mt_costs = gather_data(os.path.join(topologyOutputFolder, f"N{network_topology}D{ds}_MULTI_PATH_TWO_OUTPUT_DATA_{CREATE_NUM_REQUESTS}_{FAILURE_DISTRIBUTION}.csv"))

        global_success_so.append(so_passed)
        global_success_st.append(st_passed)
        global_success_mo.append(mo_passed)
        global_success_mt.append(mt_passed)

        global_fails_so.append(so_fails)
        global_fails_st.append(st_fails)
        global_fails_mo.append(mo_fails)
        global_fails_mt.append(mt_fails)

        global_delays_so.append(so_delays)
        global_delays_st.append(st_delays)
        global_delays_mo.append(mo_delays)
        global_delays_mt.append(mt_delays)

        global_costs_so.append(so_costs)
        global_costs_st.append(st_costs)
        global_costs_mo.append(mo_costs)
        global_costs_mt.append(mt_costs)

    for x in range(5):
        universal_success_so.append(round(sum(i[x] for i in global_success_so) / 5))
        universal_success_st.append(round(sum(i[x] for i in global_success_st) / 5))
        universal_success_mo.append(round(sum(i[x] for i in global_success_mo) / 5))
        universal_success_mt.append(round(sum(i[x] for i in global_success_mt) / 5))

        universal_fails_so.append(sum(i[x] for i in global_fails_so) / 5)
        universal_fails_st.append(sum(i[x] for i in global_fails_st) / 5)
        universal_fails_mo.append(sum(i[x] for i in global_fails_mo) / 5)
        universal_fails_mt.append(sum(i[x] for i in global_fails_mt) / 5)

        universal_delays_so.append(sum(i[x] for i in global_delays_so) / 5)
        universal_delays_st.append(sum(i[x] for i in global_delays_st) / 5)
        universal_delays_mo.append(sum(i[x] for i in global_delays_mo) / 5)
        universal_delays_mt.append(sum(i[x] for i in global_delays_mt) / 5)

        universal_costs_so.append(sum(i[x] for i in global_costs_so) / 5)
        universal_costs_st.append(sum(i[x] for i in global_costs_st) / 5)
        universal_costs_mo.append(sum(i[x] for i in global_costs_mo) / 5)
        universal_costs_mt.append(sum(i[x] for i in global_costs_mt) / 5)

    x_axis_datasets = [50, 100, 150, 200, 250]
    y_axis_requests = [50, 100, 150, 200, 250]
    y_axis_failure = [15, 25, 35, 45, 55]
    y_axis_delay = [2.0, 4.0, 6.0, 8.0, 10.0]
    y_axis_cost = [16.0, 17.0, 18.0, 19.0, 20.0]

    success_name = f'N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_success_{FAILURE_DISTRIBUTION}.png'
    fails_name = f'N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_fails_{FAILURE_DISTRIBUTION}.png'
    delays_name = f'N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_delays_{FAILURE_DISTRIBUTION}.png'
    costs_name = f'N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_costs_{FAILURE_DISTRIBUTION}.png'

    print("\n")
    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_success_so = {universal_success_so}")
    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_success_st = {universal_success_st}")
    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_success_mo = {universal_success_mo}")
    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_success_mt = {universal_success_mt}\n")

    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_fails_so = {universal_fails_so}")
    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_fails_st = {universal_fails_st}")
    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_fails_mo = {universal_fails_mo}")
    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_fails_mt = {universal_fails_mt}\n")

    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_delays_so = {universal_delays_so}")
    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_delays_st = {universal_delays_st}")
    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_delays_mo = {universal_delays_mo}")
    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_delays_mt = {universal_delays_mt}\n")

    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_costs_so = {universal_costs_so}")
    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_costs_st = {universal_costs_st}")
    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_costs_mo = {universal_costs_mo}")
    print(f"N{NETWORK_TOPOLOGY}D{start}-{stop}_universal_costs_mt = {universal_costs_mt}\n")

    create_bar_and_line_graph(universal_success_so, universal_success_st, universal_success_mo, universal_success_mt, f"NETWORK TOPOLOGY-{top_name} SATURATION: REQUESTS PASSED", "Number of Requests Processed", "Number of Successful Requests Passed", x_axis_datasets, y_axis_requests, '%', success_name)
    create_bar_and_line_graph(universal_fails_so, universal_fails_st, universal_fails_mo, universal_fails_mt, f"NETWORK TOPOLOGY-{top_name} FAILURE RANDOM: REQUEST FAILURE AVERAGES", "Number of Requests Processed", "Average Failure Probability of Requests", x_axis_datasets, y_axis_failure, '%', fails_name)
    create_bar_and_line_graph(universal_delays_so, universal_delays_st, universal_delays_mo, universal_delays_mt, f"NETWORK TOPOLOGY-{top_name} DELAYS RANDOM", "Number of Requests Processed", "Average Delay Times of Requests ms", x_axis_datasets, y_axis_delay, 'ms', delays_name)
    create_bar_and_line_graph(universal_costs_so, universal_costs_st, universal_costs_mo, universal_costs_mt, f"NETWORK TOPOLOGY-{top_name} COSTS RANDOM", "Number of Requests Processed", "Average Costs of Requests mb", x_axis_datasets, y_axis_cost, 'mb', costs_name)


def average_these(name, divisor, list_one, list_two, list_three):
    output = []
    for i in range(len(list_one)):
        a = list_one[i]
        b = list_two[i]
        c = list_three[i]

        temp = (a + b + c) / 3
        temp = f"{temp:.2f}"
        output.append(float(temp))

    print(output)


# FUNCTION THAT IS CALLED FROM main.py
def auto_generate_graphs(dataset, network_topology):
    x_axis_datasets = [50, 100, 150, 200, 250]
    y_axis_requests = [50, 100, 150, 200, 250]
    y_axis_failure = [15, 25, 35, 45, 55]
    y_axis_delay = [2.0, 4.0, 6.0, 8.0, 10.0]
    y_axis_cost = [2.0, 4.0, 6.0, 8.0, 10.0]

    SO_PASSED, SO_FAILS, SO_DELAYS, SO_COSTS = gather_data(GLOBAL_SINGLE_OUTPUT_FILE_PATH_ONE)
    ST_PASSED, ST_FAILS, ST_DELAYS, ST_COSTS = gather_data(GLOBAL_SINGLE_OUTPUT_FILE_PATH_TWO)
    MO_PASSED, MO_FAILS, MO_DELAYS, MO_COSTS = gather_data(GLOBAL_MULTI_OUTPUT_FILE_PATH_ONE)
    M2_PASSED, M2_FAILS, M2_DELAYS, M2_COSTS = gather_data(GLOBAL_MULTI_OUTPUT_FILE_PATH_TWO)

    success_name = f'D{dataset}N{network_topology}_success.png'
    fails_name = f'D{dataset}N{network_topology}_fails.png'
    delays_name = f'D{dataset}N{network_topology}_delays.png'
    costs_name = f'D{dataset}N{network_topology}_costs.png'

    create_bar_and_line_graph(SO_PASSED, ST_PASSED, MO_PASSED, M2_PASSED, "NETWORK SATURATION: REQUESTS PASSED",
                              "Number of Requests Processed", "Number of Successful Requests Passed", x_axis_datasets,
                              y_axis_requests, '%', success_name)
    create_bar_and_line_graph(SO_FAILS, ST_FAILS, MO_FAILS, M2_FAILS,
                              "NETWORK FAILURE RANDOM: REQUEST FAILURE AVERAGES", "Number of Requests Processed",
                              "Average Failure Probability of Requests", x_axis_datasets, y_axis_failure, '%',
                              fails_name)
    create_bar_and_line_graph(SO_DELAYS, ST_DELAYS, MO_DELAYS, M2_DELAYS, "NETWORK DELAYS RANDOM",
                              "Number of Requests Processed", "Average Delay Times of Requests ms", x_axis_datasets,
                              y_axis_delay, 'ms', delays_name)
    create_bar_and_line_graph(SO_COSTS, ST_COSTS, MO_COSTS, M2_COSTS, "NETWORK COSTS RANDOM",
                              "Number of Requests Processed", "Average Costs of Requests mb", x_axis_datasets,
                              y_axis_cost, 'mb', costs_name)


def gather_data(filepath):
    """
    Reads in data from a dataset and averages out the data we are measuring as lists.

    Example data:
        REQUEST STATUS,REQUEST ID,PATH ID,FAILURE PROBABILITY,DELAY,COST,FUNCTIONS,PATH
        APPROVED,1,R1P1,42.868852459016395%,10.209999999999999,7.9,['F5', 'F2', 'F1', 'F3', 'F4'],[36, 6, 44, 9]

    :param filepath: Filepath to a particular output file for a given dataset.
    :return: passed, fails, delays, costs : Lists of averages for every 50 requests.
    """
    num_passed = 0
    num_failed = 0

    passed = []
    fails = []
    delays = []
    costs = []

    with open(filepath) as fp:
        for l in range(4):
            next(fp)

        count = 1
        current_fails = 0
        current_delays = 0
        current_costs = 0
        for line in fp:
            current_elements = line.split('|')
            status = current_elements[0]

            if count % 50 == 0:
                passed.append(num_passed)

                # fails.append(current_fails / count)
                # delays.append(current_delays / count)
                # costs.append(current_costs / count)

                fails.append(current_fails / num_passed)
                delays.append(current_delays / num_passed)
                costs.append(current_costs / num_passed)

            if status == 'APPROVED':
                failure_probability = float(current_elements[3].strip(',%'))
                end_to_end_delay = float(current_elements[4].strip(','))
                request_cost = float(current_elements[5].strip(','))

                current_fails += failure_probability
                current_delays += end_to_end_delay
                current_costs += request_cost
                num_passed += 1
                count += 1
            else:
                count += 1
                num_failed += 1

    data_set_sizes = [50, 100, 150, 200, 250]

    for i in range(len(data_set_sizes)):
        num_passed = passed[i]
        size = data_set_sizes[i]
        temp = num_passed / size
        passed[i] = temp*100
        # print(f"{temp}%")

    print("{}_Passed_Requests = {}\n{}_Average_Failure = {}\n{}_Average_Delays = {}\n{}_Average_Costs = {}".format(1, passed, 1, fails, 1, delays, 1, costs))
    return passed, fails, delays, costs


def auto_label(axis, rectangle_group, notation):
    if notation != '':
        for rect in rectangle_group:     # Want to get the height of each bar.
            height = rect.get_height()
            limited_height = "{:.2f}".format(height)
            # " xy=(...), ha='center' " <-- ensures that the numbers will be perfectly centered for each bar.
            axis.annotate('{}{}'.format(limited_height, notation), xy=(rect.get_x() + rect.get_width() / 2, height), ha='center',   # (str(height), xy=(rect.get_x() + rect.get_width() / 2, height), ha='center',
                          xytext=(0, 3), textcoords='offset points',    # xytext=(0, 3) puts all text at set position.
                          color='black', fontsize=9)     # textcoords='offset points' ^^<-- Takes this xytext and offsets the text by that set amount instead.
    else:
        for rect in rectangle_group:     # Want to get the height of each bar.
            height = rect.get_height()
            # " xy=(...), ha='center' " <-- ensures that the numbers will be perfectly centered for each bar.
            axis.annotate('{}{}'.format(height, notation), xy=(rect.get_x() + rect.get_width() / 2, height), ha='center',   # (str(height), xy=(rect.get_x() + rect.get_width() / 2, height), ha='center',
                          xytext=(0, 3), textcoords='offset points',    # xytext=(0, 3) puts all text at set position.
                          color='black')     # textcoords='offset points' ^^<-- Takes this xytext and offsets the text by that set amount instead.


def create_bar_and_line_graph(single_one, single_two, multi_one, multi_two, title, xlabel, ylabel, xaxis, yaxis, notation, name):
    width = 0.2  # Width of each of the bars in bar graph
    x_single_one = [x - width for x in range(len(single_one))]  # Look at all entries of playstation and subtract our width so the bars are aligned correctly. Creates the OFFSET for each bar...
    x_multi_one = [x for x in range(len(multi_one))]  # xbox is in the middle so no need to subtract width.. <--- and ^^ both list comprehension!
    x_single_two = [x + width for x in range(len(single_two))]
    x_multi_two = [x + (width*2) for x in range(len(multi_two))]

    fig, ax = plt.subplots()  # Show both plots fig = graph, ax = axis that actually holds the data
    # NOTE: You can create multiple graphs on top of the same axis'

    # SETS THE X-AXIS FOR THE BAR GRAPHS NEW AS OF 06/21/22
    ax.set_xticks(np.arange(0, xaxis[-1]))  # [50, 100, 150, 200, 250]
    default_x_ticks = range(len(xaxis))
    plt.xticks(default_x_ticks, xaxis, fontsize=15)
    plt.yticks(fontsize=15)

    # When matplotlib creates a bar it creates a value we can store in a variable in this case rect1-rect#....
    # These variables rect1-rect3 are groups of bars. Each of these rect variables stores 4 bars.
    rect1 = ax.bar(x_single_one, single_one, width, label="Single Mapping Conventional(NOT Failure Sensitive)", color='darkslategray')  # Create bar chart
    rect2 = ax.bar(x_multi_one, multi_one, width, label="Multi Mapping Conventional(NOT Failure Sensitive)", color='limegreen')
    rect3 = ax.bar(x_single_two, single_two, width, label="Single Mapping Failure Aware", color='crimson')  # Create bar chart
    rect4 = ax.bar(x_multi_two, multi_two, width, label="Multi Mapping Failure Aware", color='skyblue')

    # ax.plot(xaxis, yaxis, label=ylabel, color='black', marker='o')  # Creates the line plot, MARKER ADDS POINTS TO LINE!

    ax.set_title(title, size=25, fontweight='bold')
    ax.set_xlabel(xlabel, size=20, fontweight='bold')
    ax.set_ylabel(ylabel, size=20, fontweight='bold')
    ax.legend(loc="lower right")  # Creates legend for labeling the different elements of the graph/plot

    auto_label(ax, rect1, notation)
    auto_label(ax, rect2, notation)
    auto_label(ax, rect3, notation)
    auto_label(ax, rect4, notation)

    if NETWORK_TOPOLOGY == 1:
        graphs_folder = os.path.join(outputFolder, "Graphs")
        specific_graphs_folder = os.path.join(graphs_folder, "small-topology")
    if NETWORK_TOPOLOGY == 2:
        graphs_folder = os.path.join(outputFolder, "Graphs")
        specific_graphs_folder = os.path.join(graphs_folder, "medium-topology")
    if NETWORK_TOPOLOGY == 3:
        graphs_folder = os.path.join(outputFolder, "Graphs")
        specific_graphs_folder = os.path.join(graphs_folder, "large-topology")
    if NETWORK_TOPOLOGY == 4:
        graphs_folder = os.path.join(outputFolder, "Graphs")
        specific_graphs_folder = os.path.join(graphs_folder, "ex-large-topology")
    if NETWORK_TOPOLOGY == 5:
        graphs_folder = os.path.join(outputFolder, "Graphs")
        specific_graphs_folder = os.path.join(graphs_folder, "ex-amass-topology")

    # plt.show()
    figure = plt.gcf()
    figure.set_size_inches(20, 11)
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    figure.show()
    manager.full_screen_toggle()
    plt.savefig(os.path.join(specific_graphs_folder, name), bbox_inches='tight', dpi=100)


################### TUTORIAL GRAPH PLZ DONT DELETE MAJOR PAIN IN THE ASS TO LOOKUP ###########################
# def tutorial_graph():
#     # X-AXIS'
#     phases = ['0', '50', '100', '150', '200', '250']    # ['Mid 90s', 'Early 2k', 'Mid 2k', 'Mid 2010s']
#     playstation = [0, 49, 92, 127, 149, 164]    # [102, 155, 87, 110]
#     xbox = [0, 49, 93, 126, 150, 166]   # [0, 24, 86, 50]
#     nintendo = [0, 49, 94, 133, 153, 170]   # [33, 22, 102, 62]
#
#     # Y-AXIS
#     pc_sales = [0, 50, 100, 150, 200, 250]  # [71, 128, 240, 316]
#
#     width = 0.2  # Width of each of the bars in bar graph
#     x_playstation = [x - width for x in range(len(playstation))]  # Look at all entries of playstation and subtract our width so the bars are aligned correctly. Creates the OFFSET for each bar...
#     x_xbox = [x for x in range(len(xbox))]    # xbox is in the middle so no need to subtract width.. <--- and ^^ both list comprehension!
#     x_nintendo = [x + width for x in range(len(nintendo))]
#
#     fig, ax = plt.subplots()    # Show both plots fig = graph, ax = axis that actually holds the data
#     # NOTE: You can create multiple graphs on top of the same axis'
#
#     # When matplotlib creates a bar it creates a value we can store in a variable in this case rect1-rect#....
#     # These variables rect1-rect3 are groups of bars. Each of these rect variables stores 4 bars.
#     rect1 = ax.bar(x_playstation, playstation, width, label="Playstation", color='darkslategray')    # Create bar chart
#     rect2 = ax.bar(x_xbox, xbox, width, label="Xbox", color='limegreen')
#     rect3 = ax.bar(x_nintendo, nintendo, width, label="nintendo", color='crimson')
#
#     ax.plot(phases, pc_sales, label="PC Sales", color='black', marker='o')   # Creates the line plot, MARKER ADDS POINTS TO LINE!
#
#     ax.set_title("The hardware market")
#     ax.set_ylabel("Total sales (in millions)")
#     ax.legend()     # Creates legend for labeling the different elements of the graph/plot
#
#     auto_label(ax, rect1)
#     auto_label(ax, rect2)
#     auto_label(ax, rect3)
#
#     # plt.grid(True)
#
#     plt.show()
################### TUTORIAL GRAPH PLZ DONT DELETE MAJOR PAIN IN THE ASS TO LOOKUP ###########################


if __name__ == '__main__':
    # gather_all_data_averages(NETWORK_TOPOLOGY)  # Creates graph for all datasets for a particular topology...

    #################### ONLY OUTPUT FOR ONE SPECIFIC DATASET AND TOPOLOGY ####################

    nt = CONSTANTS.NETWORK_TOPOLOGY
    ds = CONSTANTS.DATASET

    x_axis_datasets = [50, 100, 150, 200, 250]
    y_axis_requests = [50, 100, 150, 200, 250]
    y_axis_failure = [15, 25, 35, 45, 55]
    y_axis_delay = [2.0, 4.0, 6.0, 8.0, 10.0]
    y_axis_cost = [2.0, 4.0, 6.0, 8.0, 10.0]

    SO_PASSED, SO_FAILS, SO_DELAYS, SO_COSTS = gather_data(os.path.join(topologyOutputFolder, f"N{nt}D{ds}_SINGLE_PATH_ONE_OUTPUT_DATA_{CREATE_NUM_REQUESTS}_{FAILURE_DISTRIBUTION}.csv"))
    ST_PASSED, ST_FAILS, ST_DELAYS, ST_COSTS = gather_data(os.path.join(topologyOutputFolder, f"N{nt}D{ds}_SINGLE_PATH_TWO_OUTPUT_DATA_{CREATE_NUM_REQUESTS}_{FAILURE_DISTRIBUTION}.csv"))
    MO_PASSED, MO_FAILS, MO_DELAYS, MO_COSTS = gather_data(os.path.join(topologyOutputFolder, f"N{nt}D{ds}_MULTI_PATH_ONE_OUTPUT_DATA_{CREATE_NUM_REQUESTS}_{FAILURE_DISTRIBUTION}.csv"))
    M2_PASSED, M2_FAILS, M2_DELAYS, M2_COSTS = gather_data(os.path.join(topologyOutputFolder, f"N{nt}D{ds}_MULTI_PATH_TWO_OUTPUT_DATA_{CREATE_NUM_REQUESTS}_{FAILURE_DISTRIBUTION}.csv"))

    success_name = f'D{DATASET}N{NETWORK_TOPOLOGY}_success.png'
    fails_name = f'D{DATASET}N{NETWORK_TOPOLOGY}_fails.png'
    delays_name = f'D{DATASET}N{NETWORK_TOPOLOGY}_delays.png'
    costs_name = f'D{DATASET}N{NETWORK_TOPOLOGY}_costs.png'

    create_bar_and_line_graph(SO_PASSED, ST_PASSED, MO_PASSED, M2_PASSED, f"NETWORK TOPOLOGY-N{nt}D{ds} SATURATION: REQUESTS PASSED", "Number of Requests Processed", "Number of Successful Requests Passed", x_axis_datasets, y_axis_requests, '%', success_name)
    create_bar_and_line_graph(SO_FAILS, ST_FAILS, MO_FAILS, M2_FAILS, f"NETWORK TOPOLOGY-N{nt}D{ds} FAILURE RANDOM: REQUEST FAILURE AVERAGES", "Number of Requests Processed", "Average Failure Probability of Requests", x_axis_datasets, y_axis_failure, '%', fails_name)
    create_bar_and_line_graph(SO_DELAYS, ST_DELAYS, MO_DELAYS, M2_DELAYS, f"NETWORK TOPOLOGY-N{nt}D{ds} DELAYS RANDOM", "Number of Requests Processed", "Average Delay Times of Requests ms", x_axis_datasets, y_axis_delay, 'ms', delays_name)
    create_bar_and_line_graph(SO_COSTS, ST_COSTS, MO_COSTS, M2_COSTS, f"NETWORK TOPOLOGY-N{nt}D{ds} COSTS RANDOM", "Number of Requests Processed", "Average Costs of Requests mb", x_axis_datasets, y_axis_cost, 'mb', costs_name)