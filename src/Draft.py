"""
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

BACKUP_PATHS = []  # PLACEHOLDER for list of all

STATE_UNKNOWN = 0
POOR = 1
TURTLE = 2
FLUNK = 3
BACKUP = 4
OPTIMAL = 5

"""
For this method I assume the following:
The path parameter is traversable.
The path has enough nodes to map one function per node.
A node can have multiple functions mapped to it but it cannot map multiple functions from the same request.

Return T/F depending on if the path has enough resources to map the function
"""


def set_path_state(path):
    # Given a path must then determine and set the state of the path
    while path.state == STATE_UNKNOWN:
        if calculate_path_resources(path):
            if calculate_path_speed(path, path.delay):
                if calculate_path_failure(path, path.fail):
                    BACKUP_PATHS.append(path)
                    calculate_optimal_path()
                else:
                    print("PATH FAILURE PROBABILITY IS TOO HIGH")
                    path.state = FLUNK
            else:
                print("PATH IS TOO SLOW")
                path.state = TURTLE
        else:
            print("PATH DOES NOT HAVE ENOUGH RESOURCES")
            path.state = POOR

    print("PATH STATE HAS BEEN SET!")


def calculate_path_resources(path):
    if path.resources:
        return True
    else:
        return False


def calculate_path_speed(path, delay_threshold):
    if path.speed <= delay_threshold:
        return True
    else:
        return False


def calculate_path_failure(path, failure_threshold):
    if path.failure <= failure_threshold:
        return True
    else:
        return False


def calculate_optimal_path():
    for path in BACKUP_PATHS:
        if path.optimal:
            path.state = OPTIMAL
            # BACKUP_PATHS.pop(path)   # Basically if a path is the best one then it
            # gets set as the best one and removed from the PATHS list
        else:
            path.state = BACKUP
