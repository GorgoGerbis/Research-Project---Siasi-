from src.Request import Request
# Not a lot going on here right now going to add more to it later. - Jack


class Function(Request):

    StaticTotalFunctionsList = []

    def __init__(self, functionID, cpu, ram, buffer):
        self.functionID = functionID
        self.cpu = cpu
        self.ram = ram
        self.buffer = buffer

        Function.StaticTotalFunctionsList.append(self)