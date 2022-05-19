import matplotlib.pyplot as plt
import os

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

    # plt.grid(True)

    plt.show()


def NEW_graph():
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
    # graph()
    NEW_graph()


if __name__ == '__main__':
    run_output_graphs()
