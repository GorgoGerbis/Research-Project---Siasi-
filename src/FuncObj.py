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

class FuncObj(Enum):

    F1 = [10, 10, 10]
    F2 = [25, 25, 25]
    F3 = [45, 45, 45]
    F4 = [50, 50, 50]
    F5 = [75, 75, 75]
    F6 = [100, 100, 100]

    @enumproperty
    def RANDOM(cls):
        return random.choice(list(cls.__members__.values()))