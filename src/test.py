
# path_one_a_cost = [50, 70, 110, 70, 30, 90, 90, 70, 50, 90, 110, 70, 50, 70, 90, 70, 110, 90, 90, 110, 70, 70, 70, 130, 150, 110, 90, 90, 50, 70, 30, 70, 30, 110, 110, 70, 90, 110, 90, 50, 30, 70, 110, 90, 90, 50, 50, 70, 70, 70, 110, 90, 90	110	110	0	90	130	90	90	70	90	90	130	90	70	70	50	30	70	90	50	90	70	150	70	70	90	130	110	130	90	90	110	110	110	110	90	90	110	130	130	70	190	190	110	70, 170, 210, 110, 170, 170, 130, 90, 230]
#
# def create_figure_ONE():
#     plt.title("FIGURE 1: Number of incoming requests vs. Average delay per request")
#     plt.xlabel("Number of incoming requests")
#     plt.ylabel("Average delay per request")
#
#     path_one_delays = []
#     path_two_delays = []
#
#     path_one_avg = []
#     path_two_avg = []
#
#     for req in Request.STATIC_TOTAL_REQUEST_LIST:
#         obj = req.PATH_ONE
#         if obj is not None:
#             path_one_delays.append(obj.DELAY)
#
#     count = 0
#     total_delay_a = 0
#     for delay in path_one_delays:
#         count += 1
#         total_delay_a += delay
#         current_delay = total_delay_a / count
#         path_one_avg.append(current_delay)
#
#     for req in Request.STATIC_TOTAL_REQUEST_LIST:
#         obj = req.PATH_TWO
#         if obj is not None:
#             path_two_delays.append(obj.DELAY)
#
#     cnt = 0
#     total_delay_b = 0
#     for delay in path_two_delays:
#         cnt += 1
#         total_delay_b += delay
#         current_delay = total_delay_b / cnt
#         path_two_avg.append(current_delay)
#
#     # plt.axis([1, len(average_list_PO), 1, max_delay])
#     # plt.plot(average_list_PO)
#     # plt.plot(average_list_PT, color='r')
#     # plt.show()
#
# if __name__ == '__main__':
#     create_figure_ONE()