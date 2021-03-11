import os
import random

baseFolder = r"C:\Users\jacks\Desktop\Research Project\Research-Project---Siasi-"
resourcesFolder = os.path.join(baseFolder, "resources")
NodeInputData = os.path.join(resourcesFolder, "NodeInputData.csv")
LinkInputData = os.path.join(resourcesFolder, "LinkInputData.csv")

def createNodeInputData(number_of_nodes):
    status = ["A", "I", "R", "O"]  # Status of the node
    physical_buffer_size = [10, 20, 30, 40, 50]

    with open(NodeInputData, 'w') as fp:
        heading = "NodeId;Latitude;Longitude;Status;Resources[CPU Memory Physical Buffer " \
                  "Size];ProcessingDelay;NodeCost\n"
        fp.write(heading)

        for cnt in range(number_of_nodes):
            nodeID = cnt + 1  # Ensures we have the correct number for the node
            lat = random.randint(0, 1000)
            long = random.randint(0, 800)
            stat = status[random.randint(0, 3)]

            cpu = random.randint(0, 100)
            mem = random.randint(0, 100)
            pbs = physical_buffer_size[random.randint(0, 4)]

            resources = [cpu, mem, pbs]
            processing_delay = random.randint(0, 1000)
            nodeCost = random.randint(1, 5)

            nodeLine = "{};{};{};{};{};{};{}\n".format(nodeID, lat, long, stat, resources, processing_delay, nodeCost)
            fp.write(nodeLine)

def createLinkInputData(number_of_links, number_of_nodes):

    with open(LinkInputData, 'w') as fp:
        heading = "Source;Destination;Bandwidth;EdgeDelay;EdgeCost\n"
        fp.write(heading)

        for cnt in range(number_of_links):
            src = random.randint(1, number_of_nodes)
            dest = random.randint(1, number_of_nodes)
            bw = random.randint(0, 1000)
            ed = random.randint(0, 1000)
            ec = random.randint(0, 1000)

            linkLine = "{};{};{};{};{}\n".format(src, dest, bw, ed, ec)
            fp.write(linkLine)

if __name__ == '__main__':

    createNodeInputData(50)
    createLinkInputData(100, 50)