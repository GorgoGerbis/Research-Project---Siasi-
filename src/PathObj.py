from src.NodeObj import NodeObj
from src.FuncObj import FuncObj
from src.LinkObj import LinkObj
from src.Request import Request
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

DELAY_THRESHOLD = 25
OPTIMAL_PATH_SET = False

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

        # New stuff added today 6/18/21
        self.FAILURE_PROBABILITY = FAILURE_PROBABILITY
        self.PATH_TYPE = PATH_TYPE

        PathObj.StaticPathsList.append(self)

    def set_failure_probability(self):
        """
        We calculate the failure probability using the rule of succession formula
        created by Pierre-Simon Laplace.

        link: https://en.wikipedia.org/wiki/Rule_of_succession

        :param self: PathObj being referenced
        :return: failure_probability: an integer/double representing the probability of failure
        """

        num_trials = len(PathObj.current_path_failures)
        obj_failures = 0

        if num_trials == 0:
            self.FAILURE_PROBABILITY = 0
        else:
            for element in PathObj.current_path_failures:
                obj_failures += element[1]

            avg_failure_rate = obj_failures/num_trials
            output = (avg_failure_rate + 1) / (num_trials + 2)

            # self.FAILURE_PROBABILITY = output
            self.FAILURE_PROBABILITY = avg_failure_rate

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
        if self.PATH_TYPE != 2:
            return "Path ID: {} Route: {} State: {} REQ_FUNCTIONS: {} REQ_DELAY_THRESHOLD = {} PATH DELAY: {} PATH COST: {}\n".format(self.pathID, self.route, self.state, self.REQ_INFO[0], self.REQ_INFO[1], self.DELAY, self.COST)
        else:
            return "Path ID: {} FAILURE PROBABILITY = {}% Route: {} State: {} REQ_FUNCTIONS: {} REQ_DELAY_THRESHOLD = {} PATH DELAY: {} PATH COST: {}\n".format(self.pathID, self.FAILURE_PROBABILITY, self.route, self.state, self.REQ_INFO[0], self.REQ_INFO[1], self.DELAY, self.COST)