import os
import numpy as np
import matplotlib.pyplot as plt

baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
outputFolder = os.path.join(baseFolder, "output")


def extract_lists(input_files, line_num):
    # l1, l2, l3, l4, l5 = [], [], [], [], []
    # new_lists = [l1, l2, l3, l4, l5]
    output = []
    super_count = 0

    for filePath in input_files:
        with open(filePath) as fp:
            for i in range(line_num-1):
                fp.readline()  # <-- This is so that it skips the first line
            line = fp.readline()
            line = line.split('=')
            new_data = line[1]
            new_data = new_data[2:-2]
            new_data = new_data.split(',')
            new_list_final = []
            for val in new_data:
                new_list_final.append(float(val))
            output.append(new_list_final)
            print("HERE ---> {}".format(new_list_final))
            super_count += 1

    print("OUTPUT: {}\n".format(output))
    return output


def average_lists(l1, l2, l3, l4, l5):
    output = []
    i = 0
    for i in range(len(l1)-1):
        a, b, c, d, e = l1[i], l2[i], l3[i], l4[i], l5[i]
        temp = a + b + c + d + e
        temp = temp / 5
        output.append(temp)

    return output


if __name__ == '__main__':
    # Path One Single Mapping Costs
    input_files = [os.path.join(outputFolder, "Dataset 1 results.txt"), os.path.join(outputFolder, "Dataset 2 results.txt"), os.path.join(outputFolder, "Dataset 3 results.txt"), os.path.join(outputFolder, "Dataset 4 results.txt"), os.path.join(outputFolder, "Dataset 5 results.txt")]
    l1, l2, l3, l4, l5 = extract_lists(input_files, 4)
    l6, l7, l8, l9, l10 = extract_lists(input_files, 5)
    output_average_costs = average_lists(l1, l2, l3, l4, l5)
    output_average_costs_two = average_lists(l6, l7, l8, l9, l10)

    print("TOTAL AVERAGES FOR SINGLE MAPPING PATH ONE: {}\n".format(output_average_costs))
    print("TOTAL AVERAGES FOR SINGLE MAPPING PATH TWO: {}\n".format(output_average_costs_two))