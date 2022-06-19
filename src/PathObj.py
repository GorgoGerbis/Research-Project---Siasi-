from src.VNFObj import VNFObj
from src.NodeObj import NodeObj
from src.LinkObj import LinkObj
from src.CONSTANTS import GLOBAL_REQUEST_DELAY_THRESHOLD

"""
@author: Jackson Walker
Path resources: [CPU, RAM, Physical buffer size]

Essentially an extension of the request class. Made so that
I can keep track of things specific to a path.

In order to differentiate paths from each-other I am adding specific states that give information on where
the path ranks in usefulness and in the hierarchy of all paths for a specific request.

The criteria for a paths success is the following...
1) Travers-ability
2) Resources capability
3) Within delay threshold
4) within failure threshold
5) Processing

Once the path state is determined the paths are then able to be sorted and used.

PATH_STATE:

OPTIMAL = The best most optimal path for this request. Path that will be mapped.
BACKUP = Path meets all criteria for success but is not the most optimal
FLUNK = Meets all criteria for success EXCEPT does NOT meet failure threshold
TURTLE = Meets all criteria for success EXCEPT, delay threshold. SHOULD BE NOTED THAT FAILURE THRESHOLD IS NOT CALCULATED FOR THESE PATHS
POOR = Path is traversable but does not have enough resources
STATE_UNKNOWN = The state of the path has yet to be determined.
"""

OPTIMAL_PATH_SET = False
REQUEST_DELAY_THRESHOLD = GLOBAL_REQUEST_DELAY_THRESHOLD

# Path Object States
STATE_UNKNOWN = 0
POOR = 1
TURTLE = 2
FLUNK = 3
BACKUP = 4
OPTIMAL = 5


class PathObj:
    # STATIC LIST OF ALL OPTIMAL PATHS
    StaticOptimalPathsList = []

    # These static lists all get cleared when the optimal paths are found
    BACKUP_PATHS = []
    StaticPathsList = []
    current_path_failures = []

    current_request_paths_list = []

    def __init__(self, pathID, route, state, REQ_INFO, MAPPING_LOCATION, DELAY, COST, FAILURE_PROBABILITY, PATH_TYPE):
        """
        :param pathID: path objects name Ex: "R1P87" R# = request number P# = path number
        :param route: The list that holds the nodes being traversed in this path
        :param state: Current state of the path
        :param REQ_INFO: [request.requestedFunctions, request.request_delay_threshold, request.requestedBW]
        :param MAPPING_LOCATION: [ NodeObj, [FuncObj] ]
        :param DELAY: Total delay time of PathObj
        :param COST: Total cost of PathObj
        :param FAILURE_PROBABILITY: The probability of the path failing
        :param PATH_TYPE: Just differentiates between with or without fault tolerance
        """
        self.pathID = pathID
        self.route = route
        self.state = state
        self.REQ_INFO = REQ_INFO  # List of all the relevant information needed from the request object for path sorting
        self.MAPPING_LOCATION = MAPPING_LOCATION
        self.DELAY = DELAY
        self.COST = COST
        self.FAILURE_PROBABILITY = FAILURE_PROBABILITY
        self.PATH_TYPE = PATH_TYPE

        PathObj.StaticPathsList.append(self)
        PathObj.current_request_paths_list.append(self)

    def check_path_link_bandwidth(self):
        """
        :param req_bw:
        :param path:
        :return: Return True if links have enough bandwidth for request....
        """
        path = self.route
        req_bw = self.REQ_INFO[2]

        for i in range(len(path) - 1):
            src = path[i]
            dest = path[i + 1]
            link = LinkObj.returnLink(src, dest)

            if not link.check_enough_resources(req_bw):
                banner = "PATH{} LINK {} DID NOT HAVE ENOUGH BANDWIDTH!".format(self.pathID, link.linkID)
                print(banner)
                return False
            i += 1

        return True

    def determine_path_node_resources_MULTI(self, req_vnfs):
        """
        Tries to map as many nodes to the closest node in a path as possible.
        :param req_vnfs: A sorted array of VNF objects in order of what needs to be mapped first.
        :return: The mapping location
        """
        funcs_to_map = [VNFObj.retrieve_function_value(x) for x in req_vnfs]
        nodes = [NodeObj.returnNode(x) for x in self.route]     # Need to return only FOG Nodes NOT Terminals...
        mapping_locations = []
        i = 0

        can_map_all = True  # FINAL CHECK TO DETERMINE IF WE CAN MAP EVERYTHING

        while len(funcs_to_map) != 0 and i < len(nodes):
            cn = nodes[i]  # Current node
            cn_possible_funcs = cn.what_can_node_map_at_once(funcs_to_map)

            if len(cn_possible_funcs) != 0:
                for f in cn_possible_funcs:
                    mapping_locations.append([cn, f])
                    funcs_to_map.remove(f)

            i += 1

        if len(funcs_to_map) != 0:  # FINAL CHECK TO DETERMINE IF WE CAN MAP EVERYTHING
            can_map_all = False

        return can_map_all, mapping_locations  # <-- [ [Node, [F1: [1, 1, 0.85], F2: [2, 2, 0.75], F4: [4, 4, 0.55]>]] ]

    def determine_path_node_resources_SINGLE(self, req_vnfs):   # @ToDo lets clean this method up later...
        """
        Should try to map one VNF per node in path. THIS WORKS AS INTENDED AS OF 06/10/22!
        :param req_vnfs: A sorted array of VNF objects in order of what needs to be mapped first.
        :return:
        """
        funcs_to_map = [VNFObj.retrieve_function_value(x) for x in req_vnfs]
        nodes = [NodeObj.returnNode(x) for x in self.route]     # Need to return only FOG Nodes NOT Terminals...
        mapping_locations = []

        can_map_all = True  # FINAL CHECK TO DETERMINE IF WE CAN MAP EVERYTHING

        all_funcs_mappable = True
        i = 0  # Iterator
        breaker = 0  # Determines if we looped through multiple times trying to map the same node...

        while all_funcs_mappable and len(funcs_to_map) != 0:
            if i >= len(nodes):
                if breaker > len(nodes)*2:  # Checks if we looped through multiple times to try and map a single VNF...
                    all_funcs_mappable = False
                    can_map_all = False
                    break
                else:
                    i = 0

            cn = nodes[i]  # current node
            cf = funcs_to_map[0]  # Current function to be mapped
            pf = None  # Previous function that was mapped

            if pf is None:
                if cn.can_map(cf.value):
                    mapping_locations.append([cn, cf])
                    pf = cf
                    funcs_to_map.remove(cf)
                    breaker = 0

            elif mapping_locations[-1][0] == cn and mapping_locations[-1][1] == pf:
                super_temp = []

                for e in range(len(mapping_locations) - 1):  # FIND EACH VNF THIS NODE IS MAPPING
                    if mapping_locations[e][0] == cn:
                        super_temp.append(mapping_locations[e][1])
                super_temp.append(cf)

                if cn.can_node_map_all_funcs_given(
                        super_temp):  # Need to see if we can map multiple functions on THIS NODE
                    mapping_locations.append([cn, cf])
                    pf = cf
                    funcs_to_map.remove(cf)
                    breaker = 0
            else:
                if cn.can_map(cf.value):
                    mapping_locations.append([cn, cf])
                    pf = cf
                    funcs_to_map.remove(cf)
                    breaker = 0

            i += 1
            breaker += 1

        if len(funcs_to_map) != 0:  # FINAL CHECK TO DETERMINE IF WE CAN MAP EVERYTHING
            can_map_all = False

        return can_map_all, mapping_locations  # <-- [ [Node, [F1: [1, 1, 0.85], F2: [2, 2, 0.75], F4: [4, 4, 0.55]>]] ]

    def set_failure_probability(self):
        """
        We calculate the failure probability using the rule of succession formula
        created by Pierre-Simon Laplace.

        link: https://en.wikipedia.org/wiki/Rule_of_succession

        :param self: PathObj being referenced
        :return: failure_probability: a float representing the probability of failure
        """
        fused_path = self.create_fusion_obj_list(self.route)

        overall_average = 0
        node_count = 0

        for step in fused_path:
            if type(step) == NodeObj:
                current_fail = step.calculate_failure(step.nodeID)
                node_count += 1
                overall_average += current_fail

        node_failure_probability = overall_average / node_count
        node_failure_probability *= 100

        if node_failure_probability < 0:
            node_failure_probability *= -1

        self.FAILURE_PROBABILITY = node_failure_probability
        return node_failure_probability

    def return_failure_probability(self):
        node_failure_probability = self.set_failure_probability()
        return node_failure_probability

    @staticmethod
    def create_fusion_obj_list(path):
        links_to_get = []
        output_list = []

        for i in range(len(path) - 1):
            src = path[i]
            dest = path[i + 1]
            link = LinkObj.returnLink(src, dest)
            links_to_get.append(link)
            i += 1

        for n in path:
            node = NodeObj.returnNode(n)
            output_list.append(node)
            if len(links_to_get) != 0:
                link = links_to_get.pop(0)
                output_list.append(link)
        return output_list

    @staticmethod
    def returnOptimalPath(backup_paths_list):
        for path in backup_paths_list:
            if path.state == OPTIMAL:
                return path

    @staticmethod
    def returnPath(id):
        for p in PathObj.StaticPathsList:
            if p.pathID == id:
                return p

    def __str__(self):
        return "Path ID: {} FAILURE PROBABILITY = {}% Route: {} State: {} REQ_FUNCTIONS: {} REQ_DELAY_THRESHOLD = {} PATH DELAY: {} PATH COST: {}\n".format(
            self.pathID, self.FAILURE_PROBABILITY, self.route, self.state, self.REQ_INFO[0], self.REQ_INFO[1],
            self.DELAY, self.COST)
