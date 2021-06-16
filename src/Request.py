
class Request:

    # Static lists keeping track of all incoming requests
    STATIC_TOTAL_REQUEST_LIST = []
    STATIC_APPROVED_REQUEST_LIST = []
    STATIC_DENIED_REQUEST_LIST = []

    # @ToDo Request states that I might honestly delete bc they're unused at the moment
    REQUEST_NEEDS_CALCULATING = 0
    REQUEST_ONGOING = 1
    REQUEST_DENIED = 2
    REQUEST_APPROVED = 3

    def __init__(self, requestID, source, destination, requestedFunctions, requestedBW, requestStatus, request_delay_threshold):
        self.requestID = requestID
        self.source = source
        self.destination = destination
        self.requestedFunctions = requestedFunctions
        self.requestedBW = requestedBW
        self.requestStatus = requestStatus
        self.request_delay_threshold = request_delay_threshold

    def __str__(self):
        return "REQUEST ID: {} SOURCE: {} DESTINATION: {} FUNCTIONS: {} BANDWIDTH: {} STATUS {} DELAY THRESHOLD: {}".format(self.requestID, self.source, self.destination, self.requestedFunctions, self.requestedBW, self.requestStatus, self.request_delay_threshold)
