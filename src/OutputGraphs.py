import os
import numpy as np
import matplotlib.pyplot as plt

baseFolder = r"C:\Users\jacks\OneDrive\Desktop\Siasi Research\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
outputFolder = os.path.join(baseFolder, "output")


def auto_label(axis, rectangle_group):
    for rect in rectangle_group:     # Want to get the height of each bar.
        height = rect.get_height()
        # " xy=(...), ha='center' " <-- ensures that the numbers will be perfectly centered for each bar.
        axis.annotate(str(height),
                      xy=(rect.get_x() + rect.get_width() / 2, height),
                      ha='center',
                      xytext=(0, 3), textcoords='offset points',    # xytext=(0, 3) puts all text at set position.
                      color='gray')     # textcoords='offset points' ^^<-- Takes this xytext and offsets the text by that set amount instead.\


def graph():
    # X-AXIS'
    phases = ['Mid 90s', 'Early 2k', 'Mid 2k', 'Mid 2010s']
    playstation = [102, 155, 87, 110]
    xbox = [0, 24, 86, 50]
    nintendo = [33, 22, 102, 62]

    # Y-AXIS
    pc_sales = [71, 128, 240, 316]

    width = 0.2  # Width of each of the bars in bar graph
    x_playstation = [x - width for x in range(len(playstation))]  # Look at all entries of playstation and subtract our width so the bars are aligned correctly. Creates the OFFSET for each bar...
    x_xbox = [x for x in range(len(xbox))]    # xbox is in the middle so no need to subtract width.. <--- and ^^ both list comprehension!
    x_nintendo = [x + width for x in range(len(nintendo))]

    fig, ax = plt.subplots()    # Show both plots fig = graph, ax = axis that actually holds the data
    # NOTE: You can create multiple graphs on top of the same axis'

    # When matplotlib creates a bar it creates a value we can store in a variable in this case rect1-rect#....
    # These variables rect1-rect3 are groups of bars. Each of these rect variables stores 4 bars.
    rect1 = ax.bar(x_playstation, playstation, width, label="Playstation", color='darkslategray')    # Create bar chart
    rect2 = ax.bar(x_xbox, xbox, width, label="Xbox", color='limegreen')
    rect3 = ax.bar(x_nintendo, nintendo, width, label="nintendo", color='crimson')

    ax.plot(phases, pc_sales, label="PC Sales", color='black', marker='o')   # Creates the line plot, MARKER ADDS POINTS TO LINE!

    ax.set_title("The hardware market")
    ax.set_ylabel("Total sales (in millions)")
    ax.legend()     # Creates legend for labeling the different elements of the graph/plot

    auto_label(ax, rect1)
    auto_label(ax, rect2)
    auto_label(ax, rect3)

    plt.show()

##### TUTORIAL STUFF ##########


def create_bar_graph_COMBO_PASSED(path_one_data_single, path_two_data_single, path_one_data_multi, path_two_data_multi):
    N = 7  # was 5 before figuring out what it does
    ind = np.arange(N)
    width = 0.2
    ax1 = plt.bar(ind, path_one_data_single, width, label='Single Conventional Scheme')
    ax2 = plt.bar(np.add(ind, width), path_two_data_single, width, label='Single Fault-Aware Scheme')

    ax3 = plt.bar(ind + 0.4, path_one_data_multi, width, label='Multi Conventional Scheme')
    ax4 = plt.bar(np.add(ind + 0.4, width), path_two_data_multi, width, label='Multi Fault-Aware Scheme')

    plt.ylabel('Successful Requests')
    plt.xlabel('Incoming Requests')
    # plt.title('Success rates: Conventional mapping Vs. Fault-Aware mapping')

    plt.xticks(ind + width + 0.1, (
    '25 REQ', '50 REQ', '100 REQ', '200 REQ', '300 REQ', '400 REQ', '500 REQ', '600 REQ', '700 REQ', '800 REQ'))
    # plt.xticks(ind + width+0.1, ('25 REQ', '50 REQ', '75 REQ', '100 REQ', '200 REQ', '300 REQ', '500 REQ'))
    plt.ylim([0, 100])
    plt.legend(loc='best')

    # for bar in ax1:
    #     height = bar.get_height()
    #     plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{:.2f}%".format(height), ha='center')
    #
    # for bar in ax2:
    #     height = bar.get_height()
    #     plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{:.2f}%".format(height), ha='center')
    #
    # for bar in ax3:
    #     height = bar.get_height()
    #     plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{:.2f}%".format(height), ha='center')
    #
    # for bar in ax4:
    #     height = bar.get_height()
    #     plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{:.2f}%".format(height), ha='center')

    plt.show()


def create_bar_graph_COMBO_DELAYS(path_one_data_single, path_two_data_single, path_one_data_multi, path_two_data_multi):
    N = 7  # was 5 before figuring out what it does
    ind = np.arange(N)
    width = 0.2
    ax1 = plt.bar(ind, path_one_data_single, width, label='Single Conventional Scheme')
    ax2 = plt.bar(np.add(ind, width), path_two_data_single, width, label='Single Fault-Aware Scheme')

    ax3 = plt.bar(ind + 0.4, path_one_data_multi, width, label='Multi Conventional Scheme')
    ax4 = plt.bar(np.add(ind + 0.4, width), path_two_data_multi, width, label='Multi Fault-Aware Scheme')

    plt.ylabel('Request Delays')
    plt.xlabel('Incoming Requests')
    # plt.title('Average request delays: Conventional mapping Vs. Fault-Aware mapping')

    plt.xticks(ind + width + 0.1, ('25 REQ', '50 REQ', '75 REQ', '100 REQ', '200 REQ', '300 REQ', '500 REQ'))
    plt.ylim([0, 20])
    plt.legend(loc='best')

    # for bar in ax1:
    #     height = bar.get_height()
    #     plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{:.2f}".format(height), ha='center')
    #
    # for bar in ax2:
    #     height = bar.get_height()
    #     plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{:.2f}".format(height), ha='center')
    #
    # for bar in ax3:
    #     height = bar.get_height()
    #     plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{:.2f}".format(height), ha='center')
    #
    # for bar in ax4:
    #     height = bar.get_height()
    #     plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{:.2f}".format(height), ha='center')

    plt.show()


def create_bar_graph_COMBO_COSTS(path_one_data_single, path_two_data_single, path_one_data_multi, path_two_data_multi):
    N = 7  # was 5 before figuring out what it does
    ind = np.arange(N)
    width = 0.2
    ax1 = plt.bar(ind, path_one_data_single, width, label='Single Conventional Scheme')
    ax2 = plt.bar(np.add(ind, width), path_two_data_single, width, label='Single Fault-Aware Scheme')

    ax3 = plt.bar(ind + 0.4, path_one_data_multi, width, label='Multi Conventional Scheme')
    ax4 = plt.bar(np.add(ind + 0.4, width), path_two_data_multi, width, label='Multi Fault-Aware Scheme')

    plt.ylabel('Request Costs')
    plt.xlabel('Incoming Requests')
    # plt.title('Average request costs: Conventional mapping Vs. Fault-Aware mapping')

    plt.xticks(ind + width + 0.1, ('25 REQ', '50 REQ', '75 REQ', '100 REQ', '200 REQ', '300 REQ', '500 REQ'))
    plt.ylim([0, 70])
    plt.legend(loc='best')

    # for bar in ax1:
    #     height = bar.get_height()
    #     plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{:.2f}".format(height), ha='center')
    #
    # for bar in ax2:
    #     height = bar.get_height()
    #     plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{:.2f}".format(height), ha='center')
    #
    # for bar in ax3:
    #     height = bar.get_height()
    #     plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{:.2f}".format(height), ha='center')
    #
    # for bar in ax4:
    #     height = bar.get_height()
    #     plt.text(x=bar.get_x() + bar.get_width() / 2, y=height + .10, s="{:.2f}".format(height), ha='center')

    plt.show()


def gather_data(single, multi):
    output_single = []
    output_multi = []

    with open(single) as sp:
        sp.readline()
        sp.readline()
        sp.readline()
        sp.readline()

        count = 0
        num_passed = 0

        for line in sp:
            currentElements = line.split(',')
            temp = currentElements[0]
            count += 1
            if temp == "APPROVED":
                num_passed += 1
            if count == 10:
                output_single.append(num_passed)
                count = 0

    with open(multi) as mp:
        mp.readline()
        mp.readline()
        mp.readline()
        mp.readline()

        cnt = 0
        n_passed = 0

        for ln in mp:
            elements = ln.split(',')
            toke = elements[0]
            cnt += 1
            if toke == "APPROVED":
                n_passed += 1
            if cnt == 10:
                output_multi.append(n_passed)
                cnt = 0

    return output_single, output_multi


def create_line_graph_passed(single, multi):
    x = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    plt.plot(x, single)
    plt.plot(x, multi)
    plt.show()


def run_output_graphs():
    # single, multi = gather_data(os.path.join(outputFolder, "SINGLE_PATH_TWO_OUTPUT_DATA_100.csv"),
    #                             os.path.join(outputFolder, "MULTI_PATH_TWO_OUTPUT_DATA_100.csv"))
    # create_line_graph_passed(single, multi)
    graph()


if __name__ == '__main__':
    run_output_graphs()
    # create_bar_graph_COMBO_PASSED(single_pathOne_passed_avgs, single_pathTwo_passed_avgs, multi_pathOne_passed_avgs, multi_pathTwo_passed_avgs)
    # create_bar_graph_COMBO_DELAYS(single_pathOne_delays_avgs, single_pathTwo_delays_avgs, multi_pathOne_delays_avgs, multi_pathTwo_delays_avgs)
    # create_bar_graph_COMBO_COSTS(single_pathOne_costs_avgs, single_pathTwo_costs_avgs, multi_pathOne_costs_avgs, multi_pathTwo_costs_avgs)
