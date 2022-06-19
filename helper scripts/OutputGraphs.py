from matplotlib.ticker import FormatStrFormatter

from src.CONSTANTS import GLOBAL_SINGLE_OUTPUT_FILE_PATH_ONE, GLOBAL_SINGLE_OUTPUT_FILE_PATH_TWO
from src.CONSTANTS import GLOBAL_MULTI_OUTPUT_FILE_PATH_ONE, GLOBAL_MULTI_OUTPUT_FILE_PATH_TWO
from src.CONSTANTS import AGGREGATE_DATASETS_AVERAGES as ADA
import matplotlib.pyplot as plt


# def gather_all_data_averages(filepath, ):
#     with open(filepath, 'a') as fp:

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
                fails.append(current_fails / count)
                delays.append(current_delays / count)
                costs.append(current_costs / count)

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

    print("{}_Passed_Requests = {}\n{}_Average_Failure = {}\n{}_Average_Delays = {}\n{}_Average_Costs = {}".format(1, passed, 1, fails, 1, delays, 1, costs))
    return passed, fails, delays, costs


def auto_label(axis, rectangle_group):
    for rect in rectangle_group:     # Want to get the height of each bar.
        height = rect.get_height()
        # " xy=(...), ha='center' " <-- ensures that the numbers will be perfectly centered for each bar.
        axis.annotate(str(height),
                      xy=(rect.get_x() + rect.get_width() / 2, height),
                      ha='center',
                      xytext=(0, 3), textcoords='offset points',    # xytext=(0, 3) puts all text at set position.
                      color='black')     # textcoords='offset points' ^^<-- Takes this xytext and offsets the text by that set amount instead.


def create_bar_and_line_graph(single_one, single_two, multi_one, multi_two, title, xlabel, ylabel, xaxis, yaxis):
    width = 0.2  # Width of each of the bars in bar graph
    x_single_one = [x - width for x in range(len(single_one))]  # Look at all entries of playstation and subtract our width so the bars are aligned correctly. Creates the OFFSET for each bar...
    x_multi_one = [x for x in range(len(multi_one))]  # xbox is in the middle so no need to subtract width.. <--- and ^^ both list comprehension!
    x_single_two = [x + width for x in range(len(single_two))]
    x_multi_two = [x + width*2 for x in range(len(multi_two))]

    fig, ax = plt.subplots()  # Show both plots fig = graph, ax = axis that actually holds the data
    # NOTE: You can create multiple graphs on top of the same axis'

    # When matplotlib creates a bar it creates a value we can store in a variable in this case rect1-rect#....
    # These variables rect1-rect3 are groups of bars. Each of these rect variables stores 4 bars.
    rect1 = ax.bar(x_single_one, single_one, width, label="Single Mapping Conventional(NOT Failure Sensitive)", color='darkslategray')  # Create bar chart
    rect2 = ax.bar(x_multi_one, multi_one, width, label="Multi Mapping Conventional(NOT Failure Sensitive)", color='limegreen')
    rect3 = ax.bar(x_single_two, single_two, width, label="Single Mapping Failure Aware", color='crimson')  # Create bar chart
    rect4 = ax.bar(x_multi_two, multi_two, width, label="Multi Mapping Failure Aware", color='skyblue')

    # ax.plot(xaxis, yaxis, label=ylabel, color='black', marker='o')  # Creates the line plot, MARKER ADDS POINTS TO LINE!

    ax.set_title(title, size=18, fontweight='bold')
    ax.set_xlabel(xlabel, size=15, fontweight='bold')
    ax.set_ylabel(ylabel, size=15, fontweight='bold')
    ax.legend()  # Creates legend for labeling the different elements of the graph/plot

    auto_label(ax, rect1)
    auto_label(ax, rect2)
    auto_label(ax, rect3)
    auto_label(ax, rect4)

    plt.show()

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
    x_axis_datasets = ['50', '100', '150', '200', '250']
    y_axis_requests = [50, 100, 150, 200, 250]
    y_axis_failure = [15, 25, 35, 45, 55]   # ['15%', '25%', '35%', '45%', '55%']
    y_axis_delay = [2.0, 4.0, 6.0, 8.0, 10.0]   # ['2.0 ms', '4.0 ms', '6.0 ms', '8.0 ms', '10.ms']
    y_axis_cost = [2.0, 4.0, 6.0, 8.0, 10.0]    # ['2.0 mb', '4.0 mb', '6.0 mb', '8.0 mb', '10.mb']

    SO_PASSED, SO_FAILS, SO_DELAYS, SO_COSTS = gather_data(GLOBAL_SINGLE_OUTPUT_FILE_PATH_ONE)
    ST_PASSED, ST_FAILS, ST_DELAYS, ST_COSTS = gather_data(GLOBAL_SINGLE_OUTPUT_FILE_PATH_TWO)
    MO_PASSED, MO_FAILS, MO_DELAYS, MO_COSTS = gather_data(GLOBAL_MULTI_OUTPUT_FILE_PATH_ONE)
    M2_PASSED, M2_FAILS, M2_DELAYS, M2_COSTS = gather_data(GLOBAL_MULTI_OUTPUT_FILE_PATH_TWO)

    create_bar_and_line_graph(SO_PASSED, ST_PASSED, MO_PASSED, M2_PASSED, "REQUESTS PASSED", "Number of Requests", "Successful Requests Passed", x_axis_datasets, y_axis_requests)
    create_bar_and_line_graph(SO_FAILS, ST_FAILS, MO_FAILS, M2_FAILS, "RANDOM: FAILURE AVERAGES", "Number of Requests", "Average Request Failure Probability", x_axis_datasets, y_axis_failure)
    create_bar_and_line_graph(SO_DELAYS, ST_DELAYS, MO_DELAYS, M2_DELAYS, "DELAYS", "Number of Requests", "Average Request Delay Times", x_axis_datasets, y_axis_delay)
    create_bar_and_line_graph(SO_COSTS, ST_COSTS, MO_COSTS, M2_COSTS, "COSTS", "Number of Requests", "Average Request Costs", x_axis_datasets, y_axis_cost)

    # gather_all_data_averages(ADA, )
