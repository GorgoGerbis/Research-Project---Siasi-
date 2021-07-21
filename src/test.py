def create_figure_ONE():
    plt.title("FIGURE 1: Number of incoming requests vs. Average delay per request")
    plt.xlabel("Number of incoming requests")
    plt.ylabel("Average delay per request")

    path_one_delays = []
    path_two_delays = []

    path_one_avg = []
    path_two_avg = []

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_ONE
        if obj is not None:
            path_one_delays.append(obj.DELAY)

    count = 0
    total_delay_a = 0
    for delay in path_one_delays:
        count += 1
        total_delay_a += delay
        current_delay = total_delay_a / count
        path_one_avg.append(current_delay)

    for req in Request.STATIC_TOTAL_REQUEST_LIST:
        obj = req.PATH_TWO
        if obj is not None:
            path_two_delays.append(obj.DELAY)

    cnt = 0
    total_delay_b = 0
    for delay in path_two_delays:
        cnt += 1
        total_delay_b += delay
        current_delay = total_delay_b / cnt
        path_two_avg.append(current_delay)

    # plt.axis([1, len(average_list_PO), 1, max_delay])
    # plt.plot(average_list_PO)
    # plt.plot(average_list_PT, color='r')
    # plt.show()

if __name__ == '__main__':
    create_figure_ONE()