from src.NodeObj import NodeObj


class LinkObj(NodeObj):  # <-- This means its a subclass of NodeObj right?

    def __init__(self, linkID, linkSrc, linkDest, linkBW, linkED, linkEC, linkWeight):  # ToDo What was the difference between linkEC and linkWeight?
        self.linkID = linkID
        self.linkSrc = linkSrc
        self.linkDest = linkDest
        self.linkBW = linkBW
        self.linkED = linkED
        self.linkEC = linkEC
        self.linkWeight = linkWeight

        NodeObj.StaticLinkList.append(self)

    def showLinkSourceID(self):
        return self.linkSrc

    def compareBW(self, bw):
        if self.linkBW >= bw:
            return True
        else:
            return False

    def map_request(self, bw):
        self.linkBW = int(self.linkBW) - bw

    def check_enough_resources(self, req_bw):
        if self.compareBW(req_bw):
            # self.map_request(req_bw)
            # print("LINK {} HAS ENOUGH RESOURCES FOR TRAVERSAL FROM {} TO {}".format(self.linkID, self.linkSrc, self.linkED))
            return True
        else:
            # print("LINK {} DOES NOT ENOUGH RESOURCES FOR TRAVERSAL FROM {} TO {}".format(self.linkID, self.linkSrc, self.linkED))
            return False

    @staticmethod
    def returnLink(src, dest):
        for link in NodeObj.StaticLinkList:
            if (link.linkSrc == src and link.linkDest == dest) or (link.linkSrc == dest and link.linkDest == src):
                return link

    def __str__(self):
        string = "LinkID {} Source {} Dest {} BandWidth {} Delay {} Cost {} Weight {}".format(self.linkID, self.linkSrc, self.linkDest, self.linkBW, self.linkED, self.linkEC, self.linkWeight)
        return string
