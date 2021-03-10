from src.Request import Request

class Function(Request):

    StaticTotalFunctionsList = []

    def __init__(self, functionID, cpu, ram, buffer):
        self.functionID = functionID
        self.cpu = cpu
        self.ram = ram
        self.buffer = buffer

        Function.StaticTotalFunctionsList.append(self)