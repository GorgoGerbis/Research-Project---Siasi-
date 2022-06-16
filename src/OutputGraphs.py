from CONSTANTS import GLOBAL_SINGLE_OUTPUT_FILE_PATH_ONE, GLOBAL_SINGLE_OUTPUT_FILE_PATH_TWO
from CONSTANTS import GLOBAL_MULTI_OUTPUT_FILE_PATH_ONE, GLOBAL_MULTI_OUTPUT_FILE_PATH_TWO
import matplotlib.pyplot as plt


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

    # plt.grid(True)

    plt.show()


def NEW_graph():
    # X-AXIS'
    phases = ['0', '50', '100', '150', '250']
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

    # plt.grid(True)

    plt.show()


def gather_data(filepath):
    """
        REQUEST STATUS,REQUEST ID,PATH ID,FAILURE PROBABILITY,DELAY,COST,FUNCTIONS,PATH
        APPROVED,1,R1P1,42.868852459016395%,10.209999999999999,7.9,['F5', 'F2', 'F1', 'F3', 'F4'],[36, 6, 44, 9]
    :param filepath:
    :return:
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

            if count == 50:
                passed.append(num_passed)
                fails.append(current_fails / 50)
                delays.append(current_delays / 50)
                costs.append(current_costs / 50)

                count = 0
                current_fails = 0
                current_delays = 0
                current_costs = 0

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

    return passed, fails, delays, costs


def create_line_graph_passed(single, multi):
    x = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    plt.plot(x, single)
    plt.plot(x, multi)
    plt.show()


def run_output_graphs():
    # graph()
    NEW_graph()
    gather_data(GLOBAL_SINGLE_OUTPUT_FILE_PATH_ONE)


if __name__ == '__main__':
    SO_PASSED, SO_FAILS, SO_DELAYS, SO_COSTS = gather_data(GLOBAL_SINGLE_OUTPUT_FILE_PATH_ONE)
    ST_PASSED, ST_FAILS, ST_DELAYS, ST_COSTS = gather_data(GLOBAL_SINGLE_OUTPUT_FILE_PATH_TWO)
    MO_PASSED, MO_FAILS, MO_DELAYS, MO_COSTS = gather_data(GLOBAL_MULTI_OUTPUT_FILE_PATH_ONE)
    M2_PASSED, M2_FAILS, M2_DELAYS, M2_COSTS = gather_data(GLOBAL_MULTI_OUTPUT_FILE_PATH_TWO)

    # run_output_graphs()
