# # Online Python compiler (interpreter) to run Python online.
# # Write Python 3 code in this online editor and run it.
# goal = [1, 9]
# main_list = [[1, 2], [4, 5], [1, 4], [4, 8], [8, 9], [5, 6], [7, 2], [6, 3], [9, 7]]
#
# current_list = []
#
#
# def checkSib(aList, bList):
#     if aList[1] == bList[0]:
#         return True
#     else:
#         return False
#
#
# def findNext(a):
#     for tup in main_list:
#         if tup[0] == a:
#             return tup
#
#
# def path(a, b):
#     ugh = checkSib(a, b)
#     while not ugh:
#         current_list.append(a[0])
#         n = findNext(a[1])
#         path(n, b)
#
#
# if __name__ == '__main__':
#     a = [1, 2]
#     b = [8, 9]
#     path(a, b)
#     print(current_list)
#
