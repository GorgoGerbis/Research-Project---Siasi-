from enum import Enum
import random


class enumproperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, instance, ownerclass=None):
        if ownerclass is None:
            ownerclass = instance.__class__
        return self.fget(ownerclass)

    def __set__(self, instance, value):
        raise AttributeError("can't set pseudo-member %r" % self.name)

    def __delete__(self, instance):
        raise AttributeError("can't delete pseudo-member %r" % self.name)


class VNFObj(Enum):
    """
    Enum functions [x, y, z]
    x = CPU usage
    y = RAM usage
    z = Failure Threshold
    """
    F1 = [1, 1, 0.65]
    F2 = [2, 2, 0.55]
    F3 = [3, 3, 0.45]
    F4 = [4, 4, 0.35]
    F5 = [5, 5, 0.25]

    @enumproperty
    def RANDOM(cls):
        return random.choice(list(cls.__members__.values()))

    #######################################################################

    @staticmethod
    def retrieve_function_value(c):
        if c == 'F1' or c == "F1":
            return VNFObj.F1
        elif c == 'F2' or c == "F2":
            return VNFObj.F2
        elif c == 'F3' or c == "F3":
            return VNFObj.F3
        elif c == 'F4' or c == "F4":
            return VNFObj.F4
        elif c == 'F5' or c == "F5":
            return VNFObj.F5
        elif c == 'F6' or c == "F6":
            return VNFObj.F6
        else:
            raise AttributeError("Function {} does not exist!".format(c))


    def __str__(self):
        return "Function {} | CPU Usage: {} | RAM Usage: {} | Failure threshold: {}".format(self.name, self.value[0], self.value[1], self.value[2])

    #######################################################################
