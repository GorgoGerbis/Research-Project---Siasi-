from NodeObj import NodeObj


class LinkObj(NodeObj):  # Most likely need to make this a subclass of NodeObj

    def __init__(self, linkSrc, linkDest, linkBW, linkED, linkEC, linkWeight):
        self.linkSrc = linkSrc
        self.linkDest = linkDest
        self.linkBW = linkBW
        self.linkED = linkED
        self.linkEC = linkEC
        self.linkWeight = linkWeight

        NodeObj.StaticLinkList.append(self)

    def showLinkSourceID(self):
        return self.linkSrc

    def __str__(self):
        string = "Source {} Dest {} BandWidth {} Delay {} Cost {} Weight {}".format(self.linkSrc, self.linkDest, self.linkBW, self.linkED, self.linkEC, self.linkWeight)
        return string