from src.NodeObj import NodeObj

REQUEST_DELAY_THRESHOLD = 250.5


class RegionObj:

    STATIC_REGION_LIST = []

    def __init__(self, regionID, regionStatus, regionPosition, region_nodes, failure_probability):
        self.regionID = regionID
        self.regionStatus = regionStatus
        self.regionPosition = regionPosition
        self.region_nodes = region_nodes
        self.failure_probability = failure_probability

        RegionObj.STATIC_REGION_LIST.append(self)


    def assign_region(self, node):
        for region in RegionObj.STATIC_REGION_LIST:
            binary = self.add_region_node(node)
            if binary:
                region.regionPosition.append(node)
            else:
                continue

    def add_region_node(self, node):
        if node.check_region(self.regionPosition[0], self.regionPosition[y]):
            self.region_nodes.append(node)
        else:
            print("COULDNT ASSIGN NODE")
