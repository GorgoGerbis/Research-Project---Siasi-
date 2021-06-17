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


# ToDo I should make some help functions that retrieve all the links and nodes being used in a path.

def get_all_used(path):
    links_to_get = []

    for i in range(len(path) - 1):
        duo = [path[i], path[i + 1]]
        links_to_get.append(duo)
        i += 1

    return links_to_get


if __name__ == '__main__':
    path = ['17', '15', '8', '21', '10']
    output = get_all_used(path)
    print(output)
