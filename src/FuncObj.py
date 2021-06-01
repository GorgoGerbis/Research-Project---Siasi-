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


""" 
Enum functions [x, y, z]
x = CPU usage
y = RAM usage
z = Bandwidth taken
"""


class FuncObj(Enum):
    F1 = [1, 1, 1]
    F2 = [2, 2, 2]
    F3 = [3, 3, 3]
    F4 = [4, 4, 4]
    F5 = [5, 5, 5]
    F6 = [6, 6, 6]

    @enumproperty
    def RANDOM(cls):
        return random.choice(list(cls.__members__.values()))
