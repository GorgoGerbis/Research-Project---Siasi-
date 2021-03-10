import enum
from src.NodeObj import NodeObj


class LinkObj(NodeObj):  # Most likely need to make this a subclass of NodeObj

    def __init__(self, linkSrc, linkDest, linkBW, linkED, linkEC):
        self.linkSrc = linkSrc
        self.linkDest = linkDest
        self.linkBW = linkBW
        self.linkED = linkED
        self.linkEC = linkEC

        NodeObj.StaticLinkList.append(self)

    def showLinkSourceID(self):
        return self.linkSrc

    def __str__(self):
        string = "Source {} Dest {} BandWidth {} Delay {} Cost {} ".format(self.linkSrc, self.linkDest, self.linkBW, self.linkED, self.linkEC)
        return string